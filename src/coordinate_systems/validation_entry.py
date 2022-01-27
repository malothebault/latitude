#!/usr/bin/python3

from typing import final
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


class ValidationEntry(Gtk.Entry):
    def __init__(self, parent, max_width_char, width_char, max_length, _type, _max, popover_label = 'Exceeding maximum value'):
        Gtk.Entry.__init__(self, editable=True, can_focus=True)
        self._ = _
        self.parent = parent
        self.set_max_width_chars(max_width_char)
        self.set_width_chars(width_char)
        self.set_max_length(max_length)
        self.connect("insert_text", self.on_insert_text, _type, _max)
        self.insert_sig = self.connect("focus_out_event", self.on_focus_out)
        self.popover = Gtk.Popover.new(self)
        label = Gtk.Label(label = popover_label)
        label.set_padding(6, 8)
        label.margin = 6
        label.show_all()
        self.popover.add(label)
        self.popover.set_modal(False)
        self.popover.set_position(Gtk.PositionType.BOTTOM)
        
    def on_insert_text(self, widget, new_text, length, position, _type, _max):
        pos = widget.get_position()
        old_text = widget.get_text()
        
        if new_text == '':
            return True  
        try:
            final_text = ''.join([old_text[:pos], new_text, old_text[pos:]])
            if _type == float:
                temp = float(final_text)
            elif _type == int:
                temp = int(final_text)
            pos += 1 # increment the position of the cursor if a character is inserted
        except ValueError:
            final_text = old_text
        if final_text:
            if float(final_text) > _max:
                final_text = old_text
                self.popover.popup()
            else:
                self.popover.popdown()
            widget.handler_block_by_func(self.on_insert_text)
            widget.set_text(final_text)
            widget.handler_unblock_by_func(self.on_insert_text)
            GObject.idle_add(widget.set_position, pos)
        widget.emit_stop_by_name("insert_text")
        return True
    
    def on_focus_out(self, *args):
        self.popover.popdown()