#!/usr/bin/python3


from gi.repository import Gtk, Granite, Gdk
import constants as cn
import gi
import subprocess
import os
import locale
import gettext

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


try:
    import constants as cn
except ImportError:
    import latitude.constants as cn


class DMS(Gtk.Box):
    def __init__(self, parent):
        self.parent = parent
        self._ = _
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL, halign = Gtk.Align.START)
        
        self.lat_degree_entry = Gtk.Entry(editable=True, can_focus=True)
        self.lat_degree_entry.set_max_width_chars(5)
        self.lat_degree_entry.set_width_chars(5)
        self.lat_degree_entry.set_max_length(3)
        self.lat_degree_entry.connect("changed", self.digits_only)
        self.pack_start(self.lat_degree_entry, True, False, 0)

        self.lat_degree_label = Gtk.Label(label="°", halign=Gtk.Align.START)
        alg_label_context = self.lat_degree_label.get_style_context()
        alg_label_context.add_class("h4")
        self.pack_start(self.lat_degree_label, False, False, 5)

        self.lat_minute_entry = Gtk.Entry(editable=True, can_focus=True)
        self.lat_minute_entry.set_max_width_chars(5)
        self.lat_minute_entry.set_width_chars(5)
        self.lat_minute_entry.set_max_length(3)
        self.lat_minute_entry.connect("changed", self.digits_only)
        self.pack_start(self.lat_minute_entry, True, False, 0)

        self.lat_minute_label = Gtk.Label(label="'", halign=Gtk.Align.START)
        alg_label_context = self.lat_minute_label.get_style_context()
        alg_label_context.add_class("h4")
        self.pack_start(self.lat_minute_label, False, False, 5)
        
        self.lat_second_entry = Gtk.Entry(editable=True, can_focus=True)
        self.lat_second_entry.set_max_width_chars(5)
        self.lat_second_entry.set_width_chars(5)
        self.lat_second_entry.set_max_length(3)
        self.lat_second_entry.connect("changed", self.digits_only)
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
        
        self.lon_degree_entry = Gtk.Entry(editable=True, can_focus=True)
        self.lon_degree_entry.set_max_width_chars(5)
        self.lon_degree_entry.set_width_chars(5)
        self.lon_degree_entry.set_max_length(3)
        self.lon_degree_entry.connect("changed", self.digits_only)
        self.pack_start(self.lon_degree_entry, True, False, 0)

        self.lon_degree_label = Gtk.Label(label="°", halign=Gtk.Align.START)
        alg_label_context = self.lon_degree_label.get_style_context()
        alg_label_context.add_class("h4")
        self.pack_start(self.lon_degree_label, False, False, 5)

        self.lon_minute_entry = Gtk.Entry(editable=True, can_focus=True)
        self.lon_minute_entry.set_max_width_chars(5)
        self.lon_minute_entry.set_width_chars(5)
        self.lon_minute_entry.set_max_length(3)
        self.lon_minute_entry.connect("changed", self.digits_only)
        self.pack_start(self.lon_minute_entry, True, False, 0)

        self.lon_minute_label = Gtk.Label(label="'", halign=Gtk.Align.START)
        alg_label_context = self.lon_minute_label.get_style_context()
        alg_label_context.add_class("h4")
        self.pack_start(self.lon_minute_label, False, False, 5)
        
        self.lon_second_entry = Gtk.Entry(editable=True, can_focus=True)
        self.lon_second_entry.set_max_width_chars(5)
        self.lon_second_entry.set_width_chars(5)
        self.lon_second_entry.set_max_length(3)
        self.lon_second_entry.connect("changed", self.digits_only)
        self.pack_start(self.lon_second_entry, True, False, 0)

        self.lon_second_label = Gtk.Label(label='"', halign=Gtk.Align.START)
        alg_label_context = self.lon_second_label.get_style_context()
        alg_label_context.add_class("h4")
        self.pack_start(self.lon_second_label, False, False, 5)
        
        self.lon_combo = Gtk.ComboBoxText(can_focus=False)
        lon_combo_context = self.lon_combo.get_style_context()
        lon_combo_context.add_class("highlighted_text")
        self.lon_combo.append_text("N")
        self.lon_combo.append_text("S")
        self.lon_combo.set_active(0)
        self.pack_start(self.lon_combo, True, False, 1)
        
        self.select_file_button = Gtk.Button(image=Gtk.Image(icon_name="edit-copy", icon_size=Gtk.IconSize.BUTTON), always_show_image=True, can_focus=False)
        self.select_file_button.connect("clicked", self.parent.main_file_selection)
        # select_file_button_context = self.select_file_button.get_style_context()
        # select_file_button_context.add_class("suggested-action")
        self.pack_end(self.select_file_button, False, False, 8)
        
    # def check_integer(self, widget):
    #     try:
    #         val = int(widget.get_text()[-1])
    #         widget.set_text(str(val))
    #     except ValueError:
    #         widget.set_text('')

    def digits_only(self, widget):
        value = widget.get_text()
        #Remove non-digits from string
        value = ''.join([c for c in value if c.isdigit()]) 
        widget.set_text(value)
        return True