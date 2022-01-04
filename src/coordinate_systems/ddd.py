#!/usr/bin/python3


from gi.repository import Gtk, Granite, Gdk, GObject
import gi
import subprocess
import os
import locale
import gettext

try:
    import constants as cn
    import validation_entry as ventry
except ImportError:
    import latitude.constants as cn
    import latitude.validation_entry as ventry

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
gi.require_version('Granite', '1.0')

class DDD(Gtk.Box):
    def __init__(self, parent):
        self.parent = parent
        self._ = _
        self.first_change = True
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL, halign = Gtk.Align.START)
        
        self.lat_degree_entry = ventry.ValidationEntry(self, 9, 9, 7, float, 90, 'Max 90°')
        self.pack_start(self.lat_degree_entry, True, False, 0)

        self.lat_degree_label = Gtk.Label(label="°", halign=Gtk.Align.START)
        alg_label_context = self.lat_degree_label.get_style_context()
        alg_label_context.add_class("h4")
        self.pack_start(self.lat_degree_label, False, False, 5)
        
        self.lat_combo = Gtk.ComboBoxText(can_focus=False)
        lat_combo_context = self.lat_combo.get_style_context()
        lat_combo_context.add_class("highlighted_text")
        self.lat_combo.append_text("N")
        self.lat_combo.append_text("S")
        self.lat_combo.set_active(0)
        self.lat_combo.connect("changed", self.is_focus)
        self.pack_start(self.lat_combo, True, False, 1)
        
        self.lon_degree_label = Gtk.Label(label=",", halign=Gtk.Align.CENTER)
        alg_label_context = self.lon_degree_label.get_style_context()
        alg_label_context.add_class("h4")
        self.pack_start(self.lon_degree_label, False, False, 5)
        
        self.lon_degree_entry = ventry.ValidationEntry(self, 9, 9, 7, float, 90, 'Max 90°')
        self.pack_start(self.lon_degree_entry, True, False, 0)

        self.lon_degree_label = Gtk.Label(label="°", halign=Gtk.Align.START)
        alg_label_context = self.lon_degree_label.get_style_context()
        alg_label_context.add_class("h4")
        self.pack_start(self.lon_degree_label, False, False, 5)
        
        self.lon_combo = Gtk.ComboBoxText(can_focus=False)
        lon_combo_context = self.lon_combo.get_style_context()
        lon_combo_context.add_class("highlighted_text")
        self.lon_combo.append_text("W")
        self.lon_combo.append_text("E")
        self.lon_combo.set_active(0)
        self.lon_combo.connect("changed", self.is_focus)
        self.pack_start(self.lon_combo, True, False, 1)
        
        self.select_file_button = Gtk.Button(image=Gtk.Image(icon_name="edit-copy", icon_size=Gtk.IconSize.BUTTON), always_show_image=True, can_focus=False)
        self.select_file_button.connect("clicked", self.read_ddd)
        self.pack_end(self.select_file_button, False, False, 8)
    
    def read_ddd(self, widget):
        lat_degree = self.lat_degree_entry.get_text()
        lat_cardinal = self.lat_combo.get_active_text()
        lon_degree = self.lon_degree_entry.get_text()
        lon_cardinal = self.lon_combo.get_active_text()
        ddd = lat_degree + '°' + lat_cardinal
        ddd += ','
        ddd += lon_degree + '°' + lon_cardinal
        self.parent.clipboard.set_text(ddd, -1)
        return ddd
    
    def clear_all(self):
        self.lat_degree_entry.set_text('')
        self.lat_combo.set_active(0)
        self.lon_degree_entry.set_text('')
        self.lon_combo.set_active(0)
        return True
    
    def is_focus(self, *args):
        if self.first_change == True:
            self.parent.dms_entry.clear_all()
            self.parent.dms_entry.first_change = True
            self.parent.dmm_entry.clear_all()
            self.parent.dmm_entry.first_change = True
        self.first_change = False
        return True