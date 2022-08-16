import CardLib

class GuiLabel:

	def __init__(self, x, y, to_print):
		self.rendered_text = CardLib.gui.create_label(to_print, (255,255,255))
		(width, height) = self.rendered_text.get_size()
		self.gui_obj = CardLib.gui.GuiObject(x, y, width, height, self.gui_draw)

	def gui_draw(self):
		CardLib.gui.draw_img(self.rendered_text, self.gui_obj.x, self.gui_obj.y)
