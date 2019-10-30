# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
#
# Basic plugin template created by:
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
# Copyright (C) 2007-2008 Andrew Resch <andrewresch@gmail.com>
#
# This file is part of Deluge and is licensed under GNU General Public License 3.0, or later, with
# the additional special exception to link portions of this program with the OpenSSL library.
# See LICENSE for more details.
#

from __future__ import unicode_literals

from deluge.plugins.pluginbase import WebPluginBase
from deluge.ui.web.json_webapi import WebapiNamespace

from yarss2.util import logging

from .util.common import get_resource

log = logging.getLogger(__name__)

webapi_ns = WebapiNamespace("YaRSS2")


class YaRSS2(WebPluginBase):
    scripts = [get_resource('yarss2.js')]
    debug_scripts = scripts

    def __init__(self, name):
        super(YaRSS2, self).__init__(name)

    @webapi_ns.get
    def skrot(self):
        return "SKROT"
