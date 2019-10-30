# -*- coding: utf-8 -*-
#
# Copyright (C) 2012-2015 bendikro bro.devel+yarss2@gmail.com
#
# This file is part of YaRSS2 and is licensed under GNU General Public License 3.0, or later, with
# the additional special exception to link portions of this program with the OpenSSL library.
# See LICENSE for more details.
#

import re

import deluge.component as component

import yarss2.yarss_config
from yarss2.util import http
from yarss2.util.common import get_resource
from yarss2.util.http import urlparse

from .common import Gdk, Gtk, color_to_hex, set_tooltip_markup
from .base import DialogBase


class DialogRSSFeed(DialogBase):

    def __init__(self, gtkui, rssfeed):
        super().__init__("dialog_rssfeed.ui", "dialog_rssfeed")
        self.gtkUI = gtkui
        self.rssfeed = rssfeed
        self.builder.connect_signals({
            "on_button_cancel_clicked": self.destroy,
            "on_button_save_clicked": self.on_button_save_clicked,
            "on_dialog_rssfeed_response": self.on_dialog_response,
            "on_txt_cookies_query_tooltip": self.on_txt_cookies_query_tooltip,
            "on_checkbox_ebey_ttl_query_tooltip": self.on_checkbox_ebey_ttl_query_tooltip,
            "on_checkbox_prefer_magnet_query_tooltip": self.on_checkbox_prefer_magnet_query_tooltip,
            "on_checkbox_run_on_startup_query_tooltip": self.on_checkbox_run_on_startup_query_tooltip,
            "on_checkbox_use_cookies_toggled": self.on_checkbox_use_cookies_toggled,
        })
        self.populate_data_fields()

    def show(self):
        self.dialog.set_title("Edit Feed" if "key" in self.rssfeed else "Add Feed")
        self.dialog.set_transient_for(component.get("Preferences").pref_dialog)
        self.dialog.show()

    def set_cookies_entry_style(self):
        """
        Styles the cookies entry widget

        """
        use_cookies = self.get_object("checkbutton_use_cookies")
        cookies = self.get_object("txt_cookies")
        # Set insensitive to disable selecting text when not checked
        cookies.set_sensitive(use_cookies.get_active())

        # Get the default insensitive background color for an Entry
        test_entry = Gtk.Entry()
        style_context = test_entry.get_style_context()
        color_insensitive = style_context.get_background_color(Gtk.StateFlags.INSENSITIVE)

        inactive_color = color_to_hex(color_insensitive)

        text_color = "#b1b1b1"  # Grey-ish
        background_color = "white"

        if not use_cookies.get_active():
            text_color = inactive_color
            background_color = inactive_color

        css = (".txt_cookies_entry { color: %s; background: %s;}" % (text_color, background_color)).encode()

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def populate_data_fields(self):
        if self.rssfeed:
            self.get_object("txt_name").set_text(self.rssfeed["name"])
            self.get_object("txt_url").set_text(self.rssfeed["url"])
            self.get_object("spinbutton_updatetime").set_value(self.rssfeed["update_interval"])
            self.get_object("checkbutton_on_startup").set_active(self.rssfeed["update_on_startup"])
            self.get_object("checkbox_obey_ttl").set_active(self.rssfeed["obey_ttl"])
            self.get_object("checkbox_prefer_magnet").set_active(self.rssfeed["prefer_magnet"])
            self.get_object("checkbutton_use_cookies").set_active(self.rssfeed["use_cookies"])

            cookies = http.get_matching_cookies_dict(self.gtkUI.cookies, self.rssfeed["site"])
            cookies_hdr = http.get_cookie_header(cookies)
            self.get_object("txt_cookies").set_text(cookies_hdr.get("Cookie", ""))


            # Disable the fields field
            if "key" in self.rssfeed and self.rssfeed["key"] == yarss2.yarss_config.DUMMY_RSSFEED_KEY:
                self.get_object("txt_name").set_property("editable", False)
                self.get_object("txt_name").unset_flags(Gtk.CAN_FOCUS)
                self.get_object("txt_url").set_property("editable", False)
                self.get_object("txt_url").unset_flags(Gtk.CAN_FOCUS)
                self.get_object("spinbutton_updatetime").set_sensitive(False)
                self.get_object("checkbutton_on_startup").set_active(False)
                self.get_object("checkbutton_on_startup").set_sensitive(False)
                self.get_object("checkbox_obey_ttl").set_active(False)
                self.get_object("checkbox_obey_ttl").set_sensitive(False)
                self.get_object("checkbox_prefer_magnet").set_active(False)
                self.get_object("checkbox_prefer_magnet").set_sensitive(False)
                self.get_object("checkbutton_use_cookies").set_active(False)
                self.get_object("checkbutton_use_cookies").set_sensitive(False)
                self.get_object("button_save").set_sensitive(False)

    def get_data_fields(self, cookies=False):
        rssfeed_data = {}
        url = self.get_object("txt_url").get_text()
        # Handle spaces in url
        rssfeed_data["url"] = re.sub(r'\s', '%20', url.strip())
        rssfeed_data["site"] = urlparse.urlparse(url).netloc
        rssfeed_data["name"] = self.get_object("txt_name").get_text()
        rssfeed_data["update_interval"] = int(self.get_object("spinbutton_updatetime").get_value())
        rssfeed_data["update_on_startup"] = self.get_object("checkbutton_on_startup").get_active()
        rssfeed_data["obey_ttl"] = self.get_object("checkbox_obey_ttl").get_active()
        rssfeed_data["prefer_magnet"] = self.get_object("checkbox_prefer_magnet").get_active()
        rssfeed_data["use_cookies"]  = self.get_object("checkbutton_use_cookies").get_active()
        if cookies:
            rssfeed_data["cookies"] = self.get_object("txt_cookies").get_text()
        return rssfeed_data

    def on_button_save_clicked(self, event=None, a=None, col=None):
        rssfeed_data = self.get_data_fields()
        allowed_types = ('http', 'https', 'ftp', 'file', 'feed')
        if not urlparse.urlparse(rssfeed_data["url"])[0] in allowed_types:
            self.show_message_dialog("The RSS Feed URL must begin with one of: %s" %
                                     (", ".join(t for t in allowed_types)))
            return
        self.rssfeed.update(rssfeed_data)
        self.gtkUI.save_rssfeed(self.rssfeed)
        self.dialog.destroy()

    def on_checkbox_use_cookies_toggled(self, widget):
        self.set_cookies_entry_style()

    def on_txt_cookies_query_tooltip(self, widget, x, y, keyboard_mode, tooltip):
        return set_tooltip_markup(
            tooltip, "The cookies that match the RSS Feed URL. Manage cookies in the settings panel")

    def on_checkbox_ebey_ttl_query_tooltip(self, widget, x, y, keyboard_mode, tooltip):
        return set_tooltip_markup(
            tooltip, ("Some RSS Feeds provide a TTL value to suggest the update time to be used. "
                      "Check this to have 'update time' set to the TTL found in the RSS Feed"))

    def on_checkbox_prefer_magnet_query_tooltip(self, widget, x, y, keyboard_mode, tooltip):
        return set_tooltip_markup(
            tooltip, "If the feed contains both a torrent link and a magnet link, prefer magnet link")

    def on_checkbox_run_on_startup_query_tooltip(self, widget, x, y, keyboard_mode, tooltip):
        return set_tooltip_markup(
            tooltip, ("By checking this, the feed will be fetched when deluge is started. "
                      "Otherwise the feed will be fetched first after waiting the specified update interval."))
