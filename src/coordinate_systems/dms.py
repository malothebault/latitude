#!/usr/bin/python3


from gi.repository import Gtk, Granite, Gdk
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

class DMS(Gtk.Box):
    def __init__(self, parent):
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL, halign = Gtk.Align.START)
        self.parent = parent
        self._ = _
        
        self.lat_degree_entry = ventry.ValidationEntry(self, 5, 5, 2, int, 90, 'Max 90°')
        self.pack_start(self.lat_degree_entry, True, False, 0)

        self.lat_degree_label = Gtk.Label(label="°", halign=Gtk.Align.START)
        alg_label_context = self.lat_degree_label.get_style_context()
        alg_label_context.add_class("h4")
        self.pack_start(self.lat_degree_label, False, False, 5)

        self.lat_minute_entry = ventry.ValidationEntry(self, 5, 5, 2, int, 60, "Max 60'")
        self.pack_start(self.lat_minute_entry, True, False, 0)

        self.lat_minute_label = Gtk.Label(label="'", halign=Gtk.Align.START)
        alg_label_context = self.lat_minute_label.get_style_context()
        alg_label_context.add_class("h4")
        self.pack_start(self.lat_minute_label, False, False, 5)
        
        self.lat_second_entry = ventry.ValidationEntry(self, 7, 7, 5, float, 60, 'Max 60"')
        self.pack_start(self.lat_second_entry, True, False, 0)

        self.lat_second_label = Gtk.Label(label='"', halign=Gtk.Align.START)
        alg_label_context = self.lat_second_label.get_style_context()
        alg_label_context.add_class("h4")
        self.pack_start(self.lat_second_label, False, False, 5)
        
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
        
        self.lon_degree_entry = ventry.ValidationEntry(self, 5, 5, 2, int, 90, 'Max 90°')
        self.pack_start(self.lon_degree_entry, True, False, 0)

        self.lon_degree_label = Gtk.Label(label="°", halign=Gtk.Align.START)
        alg_label_context = self.lon_degree_label.get_style_context()
        alg_label_context.add_class("h4")
        self.pack_start(self.lon_degree_label, False, False, 5)
        
        self.lon_minute_entry = ventry.ValidationEntry(self, 5, 5, 2, int, 60, "Max 60'")
        self.pack_start(self.lon_minute_entry, True, False, 0)

        self.lon_minute_label = Gtk.Label(label="'", halign=Gtk.Align.START)
        alg_label_context = self.lon_minute_label.get_style_context()
        alg_label_context.add_class("h4")
        self.pack_start(self.lon_minute_label, False, False, 5)
        
        self.lon_second_entry = ventry.ValidationEntry(self, 7, 7, 5, float, 60, 'Max 60"')
        self.pack_start(self.lon_second_entry, True, False, 0)

        self.lon_second_label = Gtk.Label(label='"', halign=Gtk.Align.START)
        alg_label_context = self.lon_second_label.get_style_context()
        alg_label_context.add_class("h4")
        self.pack_start(self.lon_second_label, False, False, 5)
        
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
        #self.validate_button.connect("clicked", self.on_validate)
        self.pack_end(self.validate_button, False, False, 8)        
    
    def read(self):
        dms = {}
        dms['lat'] = (int(self.lat_degree_entry.get_text()),
                      int(self.lat_minute_entry.get_text()),
                      float(self.lat_second_entry.get_text()),
                      self.lat_combo.get_active_text())
        dms['lon'] = (int(self.lon_degree_entry.get_text()),
                      int(self.lon_minute_entry.get_text()),
                      float(self.lon_second_entry.get_text()),
                      self.lon_combo.get_active_text())
        return dms
    
    def write(self, dms):
        lat = dms.get('lat')
        lon = dms.get('lon')
        self.lat_degree_entry.set_text(str(lat[0]))
        self.lat_minute_entry.set_text(str(lat[1]))
        self.lat_second_entry.set_text(str(lat[2]))
        self.lat_combo.set_active(lat[3] == 'S')
        self.lon_degree_entry.set_text(str(lon[0]))
        self.lon_minute_entry.set_text(str(lon[1]))
        self.lon_second_entry.set_text(str(lon[2]))
        self.lon_combo.set_active(lon[3] == 'W')
        return True
    
    def on_copy(self, widget):
        dms = self.read()
        lat = dms.get('lat')
        lon = dms.get('lon')
        txt = f'''{lat[0]}°{lat[1]}'{lat[2]}"{lat[3]},{lon[0]}°{lon[1]}'{lon[2]}"{lon[3]}'''
        print(txt)
        self.parent.clipboard.set_text(txt, -1)
    
    def clear_all(self):
        self.lat_degree_entry.set_text('')
        self.lat_minute_entry.set_text('')
        self.lat_second_entry.set_text('')
        self.lat_combo.set_active(0)
        self.lon_degree_entry.set_text('')
        self.lon_minute_entry.set_text('')
        self.lon_second_entry.set_text('')
        self.lon_combo.set_active(0)
        return True