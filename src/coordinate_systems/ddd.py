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
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL, halign = Gtk.Align.START)
        self.parent = parent
        self._ = _
        
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
        self.lon_combo.append_text("E")
        self.lon_combo.append_text("W")
        self.lon_combo.set_active(0)
        self.pack_start(self.lon_combo, True, False, 1)
        
        self.copy_button = Gtk.Button(image=Gtk.Image(icon_name="edit-copy", icon_size=Gtk.IconSize.BUTTON), always_show_image=True, can_focus=False)
        self.copy_button.connect("clicked", self.on_copy)
        self.pack_end(self.copy_button, False, False, 1)
        
        self.validate_button = Gtk.Button(image=Gtk.Image(icon_name="process-completed", icon_size=Gtk.IconSize.BUTTON), always_show_image=True, can_focus=False)
        self.pack_end(self.validate_button, False, False, 8)  
    
    def read(self):
        ddd = {}
        ddd['lat'] = (float(self.lat_degree_entry.get_text()),
                      self.lat_combo.get_active_text())
        ddd['lon'] = (float(self.lon_degree_entry.get_text()),
                      self.lon_combo.get_active_text())
        return ddd
    
    def write(self, ddd):
        lat = ddd.get('lat')
        lon = ddd.get('lon')
        self.lat_degree_entry.set_text(str(lat[0]))
        self.lat_combo.set_active(lat[1] == 'S')
        self.lon_degree_entry.set_text(str(lon[0]))
        self.lon_combo.set_active(lon[1] == 'W')
        return True
    
    def on_copy(self, widget):
        dmm = self.read()
        lat = dmm.get('lat')
        lon = dmm.get('lon')
        txt = f'''{lat[0]}°{lat[1]},{lon[0]}°{lon[1]}'''
        print(txt)
        self.parent.clipboard.set_text(txt, -1)
    
    def clear_all(self):
        self.lat_degree_entry.set_text('')
        self.lat_combo.set_active(0)
        self.lon_degree_entry.set_text('')
        self.lon_combo.set_active(0)
        return True
