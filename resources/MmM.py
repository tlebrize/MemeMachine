import pyglet, sys, os, collections
from pyglet.window import key
from . import scene

class MemeMachine(scene.TkScene):
	
	FORMAT = ['.png', '.jpg', '.gif']

	def __init__(self, world, files_directory):
		super(MemeMachine, self).__init__(world)
		self.files_directory = files_directory
		self.entry()

	def entry(self):
		pyglet.gl.glClearColor(0, 0, 0, 0)
		self.files = collections.OrderedDict({self.files_directory + '/' + filename: None
			for filename in os.listdir(self.files_directory) if filename[-4:] in MemeMachine.FORMAT})
		if len(self.files) == 0:
			raise Exception('No files found.')
		self.current_index = 0
		self.current = None
		self.scale = 1
		self.position = (self.world.window.width // 2,
						 self.world.window.height // 2)
		self.open_file()
		self.placed = []

	def exit(self):
		del self.files
		self.current_index = 0
		self.current = None
		self.scale = 1
		self.position = (self.world.window.width // 2,
						 self.world.window.height // 2)
		self.placed = []

	def open_file(self):
		filename = list(self.files)[self.current_index]
		if self.current:
			self.position = (self.current.x, self.current.y)
			self.scale = self.current.scale
		if self.files[filename] is not None:
			self.current = self.files[filename]
		else:
			image = pyglet.image.load(filename)
			self.current = pyglet.sprite.Sprite(image)
		self.current.x = self.position[0]
		self.current.y = self.position[1]
		self.current.anchor_x = self.current.width // 2
		self.current.anchor_y = self.current.height // 2
		self.current.scale = self.scale

	def on_draw(self):
		self.world.window.clear()
		for sprite in self.placed:
			sprite.draw()
		self.current.draw()

	def on_key_press(self, symbol, modifier):
		if symbol in [48 + i for i in range(0, 10)]:
			self.current_index = (symbol - 48) % len(self.files)
			self.open_file()
		elif symbol == key.TAB:
			self.current_index = (self.current_index + 1) % len(self.files)
			self.open_file()
		elif symbol == key.Q:
			self.current.scale += 0.1
		elif symbol == key.W:
			self.current.scale -= 0.1
		elif symbol == key.UP:
			self.current.y += 25
		elif symbol == key.DOWN:
			self.current.y -= 25
		elif symbol == key.RIGHT:
			self.current.x += 25
		elif symbol == key.LEFT:
			self.current.x -= 25
		elif symbol == key.A:
			self.current.rotation += 5
		elif symbol == key.S:
			self.current.rotation -= 5
		elif symbol == key.SPACE:
			self.placed.append(self.current)
			self.current = None
			self.open_file()
		elif symbol == key.RETURN:
			pyglet.image.get_buffer_manager().get_color_buffer().save('output.png')
		elif symbol == key.ESCAPE:
			self.world.window.clear()
			self.world.transition("main")
