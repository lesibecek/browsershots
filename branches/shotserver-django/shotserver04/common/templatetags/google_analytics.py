# browsershots.org - Test your web design in different browsers
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.

"""
Include Javascript for Google Analytics.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django import template
from django.conf import settings

register = template.Library()

JAVASCRIPT = u"""
<script src="http://www.google-analytics.com/urchin.js" type="text/javascript">
</script>
<script type="text/javascript">
_uacct = "%s";
urchinTracker();
</script>
""".strip()


@register.simple_tag
def google_analytics():
    """
    Include Javascript for Google Analytics, if account is configured.
    """
    if not hasattr(settings, 'GOOGLE_ANALYTICS_ACCOUNT'):
        return ''
    if not settings.GOOGLE_ANALYTICS_ACCOUNT:
        return ''
    return JAVASCRIPT % settings.GOOGLE_ANALYTICS_ACCOUNT
