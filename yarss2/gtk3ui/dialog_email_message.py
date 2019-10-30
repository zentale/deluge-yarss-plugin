# -*- coding: utf-8 -*-
#
# Copyright (C) 2012-2019 bendikro bro.devel+yarss2@gmail.com
#
# This file is part of YaRSS2 and is licensed under GNU General Public License 3.0, or later, with
# the additional special exception to link portions of this program with the OpenSSL library.
# See LICENSE for more details.
#
import deluge.component as component

from .common import Gtk
from .base import DialogBase


class DialogEmailMessage(DialogBase):

    def __init__(self, gtkui, message_data={}):
        super().__init__("dialog_email_message.ui", "dialog_email_message")
        self.gtkUI = gtkui
        self.message_data = message_data

    def show(self):
        self.builder.connect_signals({
            "on_button_save_clicked": self.on_button_save_clicked,
            "on_button_cancel_clicked": self.destroy,
            "on_dialog_email_message_response": self.on_dialog_response,
            "on_txt_to_adress_query_tooltip": self.on_txt_to_adress_query_tooltip,
        })
        # Add data
        if self.message_data is not None:
            self.set_initial_data(self.message_data)
        self.dialog.set_transient_for(component.get("Preferences").pref_dialog)
        self.dialog.set_title("Edit Message" if "key" in self.message_data else "Add Message")
        self.dialog.show()

    def on_txt_to_adress_query_tooltip(self, widget, x, y, keyboard_mode, tooltip):
        tooltip.set_text("Separate multiple addresses with comma")
        return True

    def set_initial_data(self, data):
        self.get_object("txt_message_name").set_text(data["name"])
        self.get_object("txt_to_address").set_text(data["to_address"])
        self.get_object("txt_subject").set_text(data["subject"])
        self.get_object("checkbutton_active").set_active(data["active"])
        self.get_object("txt_email_content").get_buffer().set_text(data["message"])

    def on_button_save_clicked(self, button):
        """Saves message to config"""
        name = self.get_object("txt_message_name").get_text().strip()
        address = self.get_object("txt_to_address").get_text().strip()
        subject = self.get_object("txt_subject").get_text().strip()
        active = self.get_object("checkbutton_active").get_active()

        textbuffer = self.get_object("txt_email_content").get_buffer()
        message = textbuffer.get_text(textbuffer.get_start_iter(), textbuffer.get_end_iter(), True)

        if name == "" or address == "" or subject == "" or message == "":
            self.show_message_dialog("All fields are mandatory!")
            return

        self.message_data["name"] = name
        self.message_data["to_address"] = address
        self.message_data["subject"] = subject
        self.message_data["message"] = message
        self.message_data["active"] = active

        self.gtkUI.save_email_message(self.message_data)
        self.destroy()
