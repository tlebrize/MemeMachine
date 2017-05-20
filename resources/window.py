import pyglet

class TkWindow(pyglet.window.Window):

	def __init__(self, *args, **kwargs):
		super(TkWindow, self).__init__(*args, **kwargs)
		self.set_location(self.screen.width // 2 - self.width // 2,
						self.screen.height // 2 - self.height // 2)
		self.clear()
		self.flip()
		self.clear()
		self.set_visible(True)
