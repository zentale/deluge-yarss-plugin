from .common import Gtk

from yarss2.util.common import get_resource
from .common import show_message_dialog


class DialogBase:

    def __init__(self, ui_filename, dialog_name):
        self._builder = Gtk.Builder.new_from_file(get_resource(ui_filename))
        self.dialog = self.get_object(dialog_name)

    def get_object(self, name):
        return self._builder.get_object(name)

    @property
    def builder(self):
        return self._builder

    def destroy(self, *args):
        self.dialog.destroy()

    def on_dialog_response(self, widget, arg):
        # Escape key or close button (X in corner)
        if arg == -4:
            self.destroy()

    def show_message_dialog(self, msg):
        show_message_dialog(self.dialog, msg)
