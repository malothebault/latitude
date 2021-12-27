#!/usr/bin/python3


from gi.repository import Gtk, Granite, Gdk, GObject
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


class DDD(Gtk.Box):
    def __init__(self, parent):
        self.parent = parent
        self._ = _
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL, halign = Gtk.Align.START)
        MAX_WIDTH_CHAR = 9
        WIDTH_CHAR = 9
        MAX_LENGTH = 7
        
        self.lat_degree_entry = Gtk.Entry(editable=True, can_focus=True)
        self.lat_degree_entry.set_max_width_chars(MAX_WIDTH_CHAR)
        self.lat_degree_entry.set_width_chars(WIDTH_CHAR)
        self.lat_degree_entry.set_max_length(MAX_LENGTH)
        # self.lat_degree_entry.connect("changed", self.is_focus)
        # self.lat_degree_entry.connect("changed", self.float_only)
        # self.lat_degree_entry.connect("insert_text", self.max_90)
        self.lat_degree_entry.connect("insert_text", self.on_insert_text)
        self.pack_start(self.lat_degree_entry, True, False, 0)
        self.popover = Gtk.Popover.new(self.lat_degree_entry)
        label = Gtk.Label(label="Max 90°")
        label.show_all()
        self.popover.add(label)
        self.popover.set_modal(False)
        self.popover.set_position(Gtk.PositionType.BOTTOM)
        #self.popover.set_relative_to(self.lat_degree_entry)

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
        
        self.lon_degree_entry = Gtk.Entry(editable=True, can_focus=True)
        self.lon_degree_entry.set_max_width_chars(MAX_WIDTH_CHAR)
        self.lon_degree_entry.set_width_chars(WIDTH_CHAR)
        self.lon_degree_entry.set_max_length(MAX_LENGTH)
        self.lon_degree_entry.connect("changed", self.is_focus)
        self.lon_degree_entry.connect("changed", self.float_only)
        self.lon_degree_entry.connect("changed", self.max_90)
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
        # select_file_button_context = self.select_file_button.get_style_context()
        # select_file_button_context.add_class("suggested-action")
        self.pack_end(self.select_file_button, False, False, 8)
        
    def float_only(self, widget):
        try:
            value = widget.get_text()
            temp = float(value)
            widget.set_text(value)
        except ValueError:
            value = widget.get_text()[:-1]
            widget.set_text(value)
        return True

    def int_only(self, widget):
        value = widget.get_text()
        #Remove non-digits from string
        value = ''.join([c for c in value if c.isdigit()])
        widget.set_text(value)
        return True
    
    def max_90(self, widget, result, length, position):
        print("Hi")
        value = widget.get_text()
        self.popover.popdown()
        if value == '':
            return True
        elif float(value) > 90:
            value = value[:-1]
            self.popover.popup()
            # self.lat_degree_entry.grab_focus()
        widget.set_text(value)
        return True
    
    def max_60(self, widget):
        value = widget.get_text()
        if value == '':
            return True
        elif float(value) > 60:
            value = value[:-1]
        widget.set_text(value)
        return True
    
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
    
    def is_focus(self, widget):
        self.parent.dms_entry.clear_all()
        self.parent.dmm_entry.clear_all()
        return True
    
    def on_insert_text(self, widget, text, length, position):
        self.parent.dms_entry.clear_all()
        self.parent.dmm_entry.clear_all()
        self.popover.popdown()
        pos = widget.get_position() 
        old_text = widget.get_text()

        # Format widget text

        # First we filter digits in insertion text
        ins_dig = ''.join([c for c in text if c.isdigit()]) 
        # Second we insert digits at pos, truncate extra-digits
        new_text = ''.join([old_text[:pos], ins_dig, old_text[pos:]])[:17] 
        # Third we filter digits in `new_text`, fill the rest with underscores
        new_dig = ''.join([c for c in new_text if c.isdigit()]).ljust(13, '_')
        # We are ready to format 
        new_text = '+{0} {1} {2}-{3}'.format(new_dig[:3], new_dig[3:5], 
                                               new_dig[5:9], new_dig[9:13]).split('_')[0] 

        # Find the new cursor position

        # We get the number of inserted digits
        n_dig_ins = len(ins_dig) 
        # We get the number of digits before
        n_dig_before = len([c for c in old_text[:pos] if c.isdigit()])
        # We get the unadjusted cursor position
        new_pos = pos + n_dig_ins

        # If there was no text in the widget, we added a '+' sign, therefore move cursor
        new_pos += 1 if not old_text else 0 
        # Spacers are before digits 4, 6 and 10
        for i in [4, 6, 10]:
            # Is there spacers in the inserted text?
            if n_dig_before < i <= n_dig_before + n_dig_ins: 
                # If so move cursor
                new_pos += 1

        if new_text:
            widget.handler_block_by_func(self.on_insert_text)
            widget.set_text(new_text)
            widget.handler_unblock_by_func(self.on_insert_text)

            GObject.idle_add(widget.set_position, new_pos)

        widget.stop_emission("insert_text")
        return True