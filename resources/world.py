class TkWorld(object):

	def __init__(self, window):
		self.window = window
		self.current = None
		self.scenes = {}

	def transition(self, scene):
		if self.current:
			self.current.unload(self.window)
		self.current = self.scenes[scene]
		self.current.load(self.window)

	def add_scenes(self, new_scenes):
		self.scenes.update(new_scenes)