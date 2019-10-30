import gi  # isort:skip
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('PangoCairo', '1.0')

# isort:imports-thirdparty
from gi.repository import Gdk, GdkPixbuf, GObject, Gtk, Pango, PangoCairo  # noqa: F401


def popup_gtk_menu(menu_widget, treeview, event, expected_button=3):
    if event.button != expected_button:
        return False
    x = int(event.x)
    y = int(event.y)
    pthinfo = treeview.get_path_at_pos(x, y)
    if pthinfo is not None:
        path, col, cellx, celly = pthinfo
        treeview.grab_focus()
        treeview.set_cursor(path, col, 0)
        menu_widget.popup(None, None, None, None, event.button, event.time)
        menu_widget.show_all()
    return True


def get_selected_combobox_key(combobox, index=0):
    """Get the key of the currently selected item in the combobox"""
    # Get selected item
    model = combobox.get_model()
    iterator = combobox.get_active_iter()
    if iterator is None or model.get_value(iterator, index) == -1:
        return None
    return model.get_value(iterator, index)


def set_tooltip_markup(tooltip, markup):
    tooltip.set_markup(markup)
    return True


def color_to_hex(color):
    """
    Convert color to html hex format

    Args:
        color (Gdk.RGBA, Gdk.Color): The color to convert

    Returns:
        str: The color in hex format

    """
    if isinstance(color, Gdk.RGBA):
        color = color.to_color()
    if isinstance(color, Gdk.Color):
        floats = color.to_floats()
    else:
        return None

    def float_to_int(float):
        return int(float * 255)

    rgb = tuple([float_to_int(float) for float in floats])
    return '#%02x%02x%02x' % (rgb)


def show_message_dialog(parent, msg):
    md = Gtk.MessageDialog(parent, Gtk.DialogFlags.DESTROY_WITH_PARENT, Gtk.MessageType.INFO,
                           Gtk.ButtonsType.CLOSE, msg)
    md.set_markup(msg)
    md.run()
    md.destroy()
