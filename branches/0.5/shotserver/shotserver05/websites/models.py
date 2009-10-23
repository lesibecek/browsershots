# browsershots.org - Test your web design in different browsers
# Copyright (C) 2008 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Browsershots. If not, see <http://www.gnu.org/licenses/>.

"""
Models for the websites app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.db import models


class Domain(models.Model):
    """
    Unique domain name, without www prefix.
    """
    domain = models.CharField(max_length=200)
    submitted = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.domain


class Website(models.Model):
    """
    Website URL that was submitted for screenshots.
    """
    url = models.CharField(max_length=400)
    domain = models.ForeignKey(Domain)
    submitted = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.url