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

        '''Here we are setting some parameters for the HeaderBar
        <https://developer.gnome.org/gtk3/stable/GtkHeaderBar.html>'''
        self.set_show_close_button(True)
        self.props.title = cn.App.application_name
        
        '''THEME BUTTON'''
        self.hbar_theme = Gtk.ToolButton()
        self.hbar_theme.set_icon_name("weather-clear-night") 
        self.hbar_theme.connect(
            "clicked",
            self.on_hbar_theme_switcher
        )
        self.pack_end(self.hbar_theme)
    
    def on_hbar_theme_switcher(self, widget):
        theme = self.settings.get_property(
            "gtk-application-prefer-dark-theme"
        )
        self.settings.set_property(
            "gtk-application-prefer-dark-theme", 
            not theme # theme is a bool, we are reversing it
        )
