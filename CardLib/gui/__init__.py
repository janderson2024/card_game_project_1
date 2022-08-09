from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


from .Gui import Gui
from .gui_input import get_gui_user_input
from .gui_statics import *

__all__ = [
	"Gui",
	"get_gui_user_input"
]

_gui = Gui()

get_pygame = _gui.get_pygame

start_gui = _gui.start_gui

redraw = _gui.redraw

add_obj_to_be_drawn = _gui.add_obj_to_be_drawn

remove_obj_from_being_drawn = _gui.remove_obj_from_being_drawn

remove_all_obj = _gui.remove_all_obj

draw_rect = _gui.draw_rect

draw_img = _gui.draw_img
