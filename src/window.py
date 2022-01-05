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
import locale
import os
import gettext
import constants as cn
import dms 
import dmm
import ddd
import converter

gi.require_version('Gtk', '3.0')
# gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Granite, Gdk

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

class Window(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title=cn.App.application_name)
        self._ = _
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        
        context = self.get_style_context()
        context.add_class ("rounded")

        '''Here we are creating a new instance of Headerbar 
        and setting as the titlebar'''
        # self.hbar = hb.Headerbar(self)
        # self.set_titlebar(self.hbar)
        self.headerbar = Gtk.HeaderBar(decoration_layout_set=True, decoration_layout="close:")
        headerbar_context = self.headerbar.get_style_context()
        headerbar_context.add_class("flat")
        self.headerbar.set_show_close_button(True)
        self.headerbar.props.title = cn.App.application_name
        #self.headerbar.set_custom_title("Latitude")
        self.set_titlebar(self.headerbar)
        
        self.set_border_width(80)
        self.set_resizable(False)

        self.vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 20, homogeneous = False, valign = Gtk.Align.CENTER)
        vbox_context = self.vbox.get_style_context()
        vbox_context.add_class("main_content")

        self.select_file_button = Gtk.Button(label=_("Select File"),image=Gtk.Image(icon_name="document-open-symbolic", icon_size=Gtk.IconSize.BUTTON), always_show_image=True, can_focus=False)
        self.select_file_button.connect("clicked", self.main_file_selection)
        select_file_button_context = self.select_file_button.get_style_context()
        select_file_button_context.add_class("suggested-action")
        
        self.converter = converter.Converter()
        
        self.dms_entry = dms.DMS(self)
        self.dmm_entry = dmm.DMM(self)
        self.ddd_entry = ddd.DDD(self)
        
        self.dms_entry.validate_button.connect("clicked", self.on_validate_dms)
        self.dmm_entry.validate_button.connect("clicked", self.on_validate_dmm)
        self.ddd_entry.validate_button.connect("clicked", self.on_validate_ddd)

        self.vbox.pack_start(self.dms_entry, False, False, 1)
        self.vbox.pack_start(self.dmm_entry, False, False, 1)
        self.vbox.pack_start(self.ddd_entry, False, False, 1)
        
        self.add(self.vbox)
        
    def main_file_selection(self, button):
        dialog = Gtk.FileChooserNative.new(_("Please choose a file"), self, Gtk.FileChooserAction.OPEN, _("Open"), _("Cancel"))
        response = dialog.run()

        if response == Gtk.ResponseType.ACCEPT:
                print("Hello")

        dialog.destroy()
        
    def on_validate_dms(self, *args):
        dmm = self.converter.dms2dmm(self.dms_entry.read())
        self.dmm_entry.write(dmm)
        ddd = self.converter.dms2ddd(self.dms_entry.read())
        self.ddd_entry.write(ddd)
        return True
    
    def on_validate_dmm(self, *args):
        dms = self.converter.dmm2dms(self.dmm_entry.read())
        self.dms_entry.write(dms)
        ddd = self.converter.dmm2ddd(self.dmm_entry.read())
        self.ddd_entry.write(ddd)
        return True
    
    def on_validate_ddd(self, *args):
        dms = self.converter.ddd2dms(self.ddd_entry.read())
        self.dms_entry.write(dms)
        dmm = self.converter.ddd2dmm(self.ddd_entry.read())
        self.dmm_entry.write(dmm)
        return True