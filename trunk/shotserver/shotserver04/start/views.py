# browsershots.org - Test your web design in different browsers
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
Browsershots front page.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from datetime import datetime, timedelta
from django.db import transaction
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from shotserver04 import settings
from shotserver04.common import int_or_none, last_poll_timeout, error_page
from shotserver04.common.preload import preload_foreign_keys
from shotserver04.start.models import NewsItem
from shotserver04.start.forms.url import UrlForm
from shotserver04.start.forms.browsers import BrowsersForm
from shotserver04.start.forms.features import FeaturesForm
from shotserver04.start.forms.options import OptionsForm
from shotserver04.factories.models import Factory
from shotserver04.platforms.models import Platform
from shotserver04.browsers.models import BrowserGroup, Browser
from shotserver04.requests.models import RequestGroup, Request
from shotserver04.sponsors.models import Sponsor

BROWSER_COLUMNS = 5
SELECTOR_TEMPLATE = u"""
<a href="javascript:select_browsers('%s')" onfocus="this.blur()">%s</a>
""".strip()


def start(http_request):
    """
    Front page with URL input, browser chooser, and options.
    """
    # Initialize forms.
    post = http_request.POST or None
    url_form = UrlForm(post)
    features_form = FeaturesForm(post)
    options_form = OptionsForm(post)
    # Get available choices from database, with correct translations.
    active_factories = Factory.objects.filter(
        last_poll__gte=last_poll_timeout())
    active_browsers = Browser.objects.filter(
        factory__in=active_factories,
        active=True)
    if not active_browsers:
        return error_page(http_request, _("out of service"),
            _("No active screenshot factories."),
            _("Please try again later."))
    features_form.load_choices(active_browsers)
    options_form.load_choices(active_factories)
    # Validate posted data.
    valid_post = (url_form.is_valid() and
                  options_form.is_valid() and
                  features_form.is_valid())
    # Preload some database entries for browser forms
    preload_foreign_keys(active_browsers,
                         factory=active_factories,
                         factory__operating_system=True,
                         browser_group=True)
    # Browser forms for each platform.
    browser_forms = []
    for platform in Platform.objects.all():
        browser_form = BrowsersForm(active_browsers, platform, post)
        browser_form.platform_name = \
            unicode(platform).lower().replace(' ', '-')
        if browser_form.is_bound:
            browser_form.full_clean()
        if browser_form.fields:
            browser_forms.append(browser_form)
        valid_post = valid_post and browser_form.is_valid()
    browser_forms[0].is_first = True
    browser_forms[-1].is_last = True
    if not valid_post:
        # Show HTML form.
        if 'url' in http_request.GET:
            url_form.fields['url'].initial = http_request.GET['url']
        multi_column(browser_forms)
        selectors = ' |\n'.join(selector_links(browser_forms))
        news_list = NewsItem.objects.all()[:10]
        sponsors_list = Sponsor.objects.filter(front_page=True)
        return render_to_response('start/start.html', locals(),
            context_instance=RequestContext(http_request))
    # Create screenshot requests and redirect to website overview.
    expire = datetime.now() + timedelta(minutes=30)
    values = {
        'website': url_form.cleaned_data['website'],
        'ip': http_request.META['REMOTE_ADDR'],
        'user': None,
        }
    if http_request.user.is_authenticated():
        values['user'] = http_request.user
    values.update(options_form.cleaned_data)
    values.update(features_form.cleaned_data)
    match_values = {}
    for key in values:
        if values[key] is None:
            match_values[key + '__isnull'] = True
        else:
            match_values[key] = values[key]
    existing = RequestGroup.objects.filter(
        expire__gte=datetime.now(), **match_values).order_by('-submitted')
    if len(existing):
        request_group = existing[0]
        request_group.expire = expire
        request_group.save()
    else:
        request_group = RequestGroup.objects.create(expire=expire, **values)
    priority = domain_priority(url_form.cleaned_data['domain'].name) and 1 or 0
    for browser_form in browser_forms:
        create_platform_requests(
            request_group, browser_form.platform, browser_form, priority)
    # Make sure that the redirect will show the new request group
    transaction.commit()
    # return render_to_response('debug.html', locals(),
    #     context_instance=RequestContext(http_request))
    return HttpResponseRedirect(values['website'].get_absolute_url())


def domain_priority(domain_name):
    """
    Check if domain priority is enabled for this domain name.
    """
    return (hasattr(settings, 'PRIORITY_DOMAINS') and
            domain_name in settings.PRIORITY_DOMAINS and
            settings.PRIORITY_DOMAINS[domain_name] > datetime.now())


def multi_column(browser_forms):
    """
    Arrange browsers in multiple columns per platform.
    """
    groups = [[form.column_length(), form] for form in browser_forms]
    for total_columns in range(len(browser_forms), BROWSER_COLUMNS):
        groups.sort()
        length, form = groups[-1]
        if length <= 4:
            break
        form.columns += 1
        groups[-1][0] = form.column_length()


def selector_links(browser_forms):
    """
    Links to select or unselect all browsers.
    """
    total = sum([len(form.fields) for form in browser_forms])
    yield SELECTOR_TEMPLATE % ('+' * total, capfirst(_('select all')))
    yield SELECTOR_TEMPLATE % ('-' * total, capfirst(_('deselect all')))


def create_platform_requests(request_group, platform, browser_form,
                             priority=0):
    """
    Create screenshots requests for selected browsers on one platform.
    """
    platform_lower = platform.name.lower().replace(' ', '-')
    for name in browser_form.fields:
        if not browser_form.cleaned_data[name]:
            continue # Browser not selected
        first_part, browser_name, major, minor = name.split('_')
        if first_part != platform_lower:
            continue # Different platform
        browser_group = BrowserGroup.objects.get(
            name__iexact=browser_name.replace('-', ' '))
        Request.objects.get_or_create(
            request_group=request_group,
            platform=platform,
            browser_group=browser_group,
            major=int_or_none(major),
            minor=int_or_none(minor),
            priority=priority,
            )
