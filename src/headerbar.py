#!/usr/bin/python3
'''
   Copyright 2017 Mirko Brombin <send@mirko.pm>

   This file is part of ElementaryPython.

    ElementaryPython is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ElementaryPython is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ElementaryPython.  If not, see <http://www.gnu.org/licenses/>.
'''

from ast import Gt
import gi
import webbrowser
import os
import locale
import gettext
import constants as cn

########### TRANSLATION ##############
try:
    current_locale, encoding = locale.getdefaultlocale()
    locale_path = os.path.join(
        os.path.abspath(
            os.path.dirname(__file__)
        ),
        'locale'
    )
    translate = gettext.translation(
        cn.App.application_shortname,
        locale_path,
        [current_locale]
    )
    _ = translate.gettext
except FileNotFoundError:
    _ = str
######################################

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, Gio

import constants as cn

class Headerbar(Gtk.HeaderBar):

    def __init__(self, parent):

        Gtk.HeaderBar.__init__(self)
        self.parent = parent
        self._ = _
        self.settings = Gio.Settings(schema_id="com.github.malothebault.latitude")
        
        # self.headerbar = Gtk.HeaderBar(decoration_layout_set=True, decoration_layout="close:")
        headerbar_context = self.get_style_context()
        headerbar_context.add_class("flat")
        self.set_show_close_button(True)
        self.props.title = cn.App.application_name
 
        #Creating and placing a button
        self.button = Gtk.ToolButton()
        self.button.set_icon_name("open-menu")
        self.button.connect("clicked", self.on_click)
        self.pack_end(self.button)
        
        #Creating a popover
        self.popover = Gtk.PopoverMenu.new()
        self.popover.set_relative_to(self.button)        

        margin_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        margin_box.set_property('margin', 10)
        self.popover.add(margin_box)
        
        grid = Gtk.Grid()
        grid.set_row_spacing(6)
        grid.set_column_spacing(12)
        
        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        
        label = Gtk.Label(label = _("Map provider : "))
        label.set_padding(6, 6)
        
        map_providers = [
            "OpenStreetMap",
            "Google",
            "Qwant"
        ]
        map_combo = Gtk.ComboBoxText()
        map_combo.set_entry_text_column(0)
        map_combo.connect("changed", self.on_map_combo_changed)
        for map_provider in map_providers:
            map_combo.append_text(map_provider)
        map_combo.set_active(map_providers.index(self.settings.get_string("map-provider")))
        
        hbox.pack_start(label, False, False, 0)
        hbox.pack_start(map_combo, False, False, 0)
        
        info_button = Gtk.Button(label=_("Geographic Coordinate System"),
                                 image=Gtk.Image(icon_name="dialog-information",
                                                 icon_size=Gtk.IconSize.BUTTON),
                                 always_show_image=True,
                                 can_focus=False)
        info_button.set_tooltip_text(_("Get more information about geographic coordinate system"))
        info_button.connect("clicked", self.on_info_button_clicked)
        
        grid.attach(hbox, 0, 0, 1, 1)
        grid.attach(info_button, 0, 1, 1, 1)
        margin_box.pack_start(grid, False, False, 0)
    
    def on_info_button_clicked(self, widget):
        webbrowser.open_new_tab(
                f"https://en.wikipedia.org/wiki/Geographic_coordinate_system"
            )
        return True
        
    def on_click(self, button):
    #Toggle
        if self.popover.get_visible():
            self.popover.hide()
        else:
            self.popover.show_all()
            
    def on_map_combo_changed(self, combo):
        text = combo.get_active_text()
        if text is not None:
            print("Selected: currency=%s" % text)
            self.parent.map_provider = text
