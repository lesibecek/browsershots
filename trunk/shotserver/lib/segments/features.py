# -*- coding: utf-8 -*-
# browsershots.org
# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
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
Drop-down boxes for browser features.
"""

__revision__ = '$Rev: 41 $'
__date__ = '$Date: 2006-03-15 07:46:49 +0100 (Wed, 15 Mar 2006) $'
__author__ = '$Author: johann $'

from shotserver03.interface import xhtml

def write_select(name, options, selected = None):
    """
    Write XHTML drop-down input.
    """
    xhtml.write_open_tag_line('select', _name=name)
    for index, option in enumerate(options.split('|')):
        value, text = option.split('=')
        if selected and index == selected - 1:
            xhtml.write_tag_line('option', text, value=value, selected="selected")
        else:
            xhtml.write_tag_line('option', text, value=value)
    xhtml.write_close_tag_line('select')

def write():
    """
    Write drop-down boxes for browser features.
    """
    xhtml.write_open_tag_line('div', _class="gray background", _id="features")

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Screen resolution")
    xhtml.write_tag_line('br')
    write_select('width', "tiny=Tiny (640x480)|small=Small (800x600)|medium=Medium (1024x768)" +
                 "|large=Large (1280x1024)|huge=Huge (1600x1200)", 3)
    xhtml.write_close_tag_line('div')

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "JavaScript")
    xhtml.write_tag_line('br')
    write_select('js', "dontcare=Don't Care|no=Disabled|yes=Enabled|1.3=Version 1.3|1.4=Version 1.4|" +
                 "1.5=Version 1.5|1.6=Version 1.6", 3)
    xhtml.write_close_tag_line('div')

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Macromedia Flash")
    xhtml.write_tag_line('br')
    write_select('flash', "dontcare=Don't Care|no=Not Installed|yes=Installed|4=Version 4|5=Version 5|6=Version 6" +
                 "|7=Version 7|8=Version 8", 3)
    xhtml.write_close_tag_line('div')

    # If jobs can't be finished soon enough, they will be removed from the queue.
    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Maximum wait")
    xhtml.write_tag_line('br')
    write_select('expire', "15=15 minutes|30=30 minutes|60=1 hour|120=2 hours|240=4 hours", 2)
    xhtml.write_close_tag_line('div')

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Color depth")
    xhtml.write_tag_line('br')
    write_select('bpp', "dontcare=Don't Care|4=4 Bits (16 Colors)|8=8 Bits (256 Colors)|" +
                 "16=16 Bits (High Color)|24=24 Bits (True Color)")
    xhtml.write_close_tag_line('div')

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Java")
    xhtml.write_tag_line('br')
    write_select('java', "dontcare=Don't Care|no=Not Installed|yes=Installed|blackdown=Blackdown|kaffe=Kaffe|sun=Sun Java" +
                 "|sun_1.2=Sun Java 1.2|sun_1.3=Sun Java 1.3|sun_1.4=Sun Java 1.4|sun_5.0=Sun Java 5.0")
    xhtml.write_close_tag_line('div')

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Media plugins")
    xhtml.write_tag_line('br')
    write_select('media', "dontcare=Don't Care|quicktime=Apple Quicktime|wmp=Windows Media Player|svg=SVG|pdf=PDF")
    xhtml.write_close_tag_line('div')

    xhtml.write_tag_line('div', '', _class="clear")
    xhtml.write_close_tag_line('div') # id="features"
