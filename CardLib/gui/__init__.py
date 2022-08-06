from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


from .Gui import Gui
from .gui_input import get_gui_user_input

__all__ = [
	"Gui",
	"get_gui_user_input"
]
