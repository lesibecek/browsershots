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
PayPal models.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.db import models


class PayPalLog(models.Model):
    """
    Database log for PayPal IPN (instant payment notification).
    """
    raw_post_data = models.CharField(maxlength=2000)
    response = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(maxlength=200, blank=True)
    last_name = models.CharField(maxlength=200, blank=True)
    residence_country = models.CharField(maxlength=200, blank=True)
    charset = models.CharField(maxlength=200, blank=True)

    test_ipn = models.CharField(maxlength=200, blank=True)
    txn_id = models.CharField(maxlength=200, blank=True)
    txn_type = models.CharField(maxlength=200, blank=True)
    item_name = models.CharField(maxlength=200, blank=True)
    item_number = models.CharField(maxlength=200, blank=True)
    memo = models.CharField(maxlength=200, blank=True)

    mc_currency = models.CharField(maxlength=200, blank=True)
    mc_gross = models.CharField(maxlength=200, blank=True)
    mc_fee = models.CharField(maxlength=200, blank=True)

    payment_date = models.CharField(maxlength=200, blank=True)
    payment_type = models.CharField(maxlength=200, blank=True)
    payment_fee = models.CharField(maxlength=200, blank=True)
    payment_gross = models.CharField(maxlength=200, blank=True)
    payment_status = models.CharField(maxlength=200, blank=True)
    pending_reason = models.CharField(maxlength=200, blank=True)

    payer_id = models.CharField(maxlength=200, blank=True)
    payer_email = models.CharField(maxlength=200, blank=True)
    payer_status = models.CharField(maxlength=200, blank=True)

    receiver_id = models.CharField(maxlength=200, blank=True)
    receiver_email = models.CharField(maxlength=200, blank=True)

    class Meta:
        verbose_name = 'PayPal log'
        verbose_name_plural = 'PayPal logs'

    class Admin:
        list_display = ('txn_id', 'payment_date', 'payer_email',
                        'mc_currency', 'mc_gross', 'payment_status',
                        'response', 'posted')