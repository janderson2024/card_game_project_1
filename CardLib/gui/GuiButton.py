import CardLib

class GuiButton:

	def __init__(self, button_text, x=0, y=0, text_color=(255,255,255), button_background=(100,100,100)):
		self.rendered_text = CardLib.gui.create_label(button_text, text_color, button_background)
		(width, height) = self.rendered_text.get_size()
		self.gui_obj = CardLib.gui.GuiObject(x, y, width, height, self.gui_draw)

	def gui_draw(self):
		CardLib.gui.draw_img(self.rendered_text, self.gui_obj.x, self.gui_obj.y)
