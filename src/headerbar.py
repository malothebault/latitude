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

from gi.repository import Gtk, Gdk

import constants as cn

class Headerbar(Gtk.HeaderBar):

    '''Getting system default settings'''
    settings = Gtk.Settings.get_default()

    def __init__(self, parent):

        Gtk.HeaderBar.__init__(self)
        self.parent = parent
        self._ = _
        
        # self.headerbar = Gtk.HeaderBar(decoration_layout_set=True, decoration_layout="close:")
        headerbar_context = self.get_style_context()
        headerbar_context.add_class("flat")
        self.set_show_close_button(True)
        self.props.title = cn.App.application_name
        
        '''THEME BUTTON'''
        self.hbar_theme = Gtk.ToolButton()
        self.hbar_theme.set_icon_name("weather-clear-night") 
        self.hbar_theme.connect(
            "clicked",
            self.on_hbar_theme_switcher
        )
        # self.pack_end(self.hbar_theme)
 
        #Creating and placing a button
        self.button = Gtk.ToolButton()
        self.button.set_icon_name("preferences-system")
        self.button.connect("clicked", self.on_click)
        self.pack_end(self.button)
        
        #Creating a popover
        self.popover = Gtk.PopoverMenu.new()
        self.popover.set_relative_to(self.button)        
        
        grid = Gtk.Grid()
        grid.set_row_spacing(6)
        grid.set_column_spacing(12)
        # pbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        # self.popover.add(pbox)
        
        # phbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        # self.popover.add(phbox)
        # pbox.pack_end(phbox, False, False, 1)
        
        map_providers = [
            "Google",
            "OpenStreetMap",
            "DuckDuckGo",
            "Qwant"
        ]
        map_combo = Gtk.ComboBoxText()
        map_combo.set_entry_text_column(0)
        map_combo.connect("changed", self.on_map_combo_changed)
        for map_provider in map_providers:
            map_combo.append_text(map_provider)
        map_combo.set_active(0)
        
        # one = Gtk.ModelButton.new()
        # one.set_label("Button One")
        # pbox.pack_start(self.map_combo, False, False, 0)
        
        two = Gtk.ModelButton.new()
        two.set_label("Button Two")
        # pbox.pack_start(two, False, False, 0)
        
        three = Gtk.ToolButton()
        three.set_icon_name("dialog-information")
        # pbox.pack_start(three, False, False, 0)
        grid.attach(map_combo, 0, 0, 2, 1)
        grid.attach(self.hbar_theme, 0, 1, 1, 1)
        grid.attach(three, 1, 1, 1, 1)
        self.popover.add(grid)
    
    def on_hbar_theme_switcher(self, widget):
        theme = self.settings.get_property(
            "gtk-application-prefer-dark-theme"
        )
        self.settings.set_property(
            "gtk-application-prefer-dark-theme", 
            not theme # theme is a bool, we are reversing it
        )
        
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
