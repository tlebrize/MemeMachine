import pyglet, sys, os, collections
from pyglet.window import key

class Viewer(pyglet.window.Window):
	def __init__(self, files_directory):
		super(Viewer, self).__init__(800, 800, resizable=True)
		self.format = ['.png', '.jpg', '.gif']
		i = 0
		self.files = collections.OrderedDict({files_directory + '/' + filename: None
			for filename in os.listdir(files_directory) if filename[-4:] in self.format})
		if len(self.files) == 0:
			raise Exception('No files found.')
		for filename in self.files:
			print(i, ':', filename)
			i += 1
		self.current_index = 0
		self.current = None
		self.scale = 1
		self.position = (self.width // 2, self.height // 2)
		self.load()
		self.placed = []

	def load(self):
		filename = list(self.files)[self.current_index]
		if self.current:
			self.position = (self.current.x, self.current.y)
			self.scale = self.current.scale
		if self.files[filename] is not None:
			self.current = self.files[filename]
		else:
			if '.gif' in filename[-4:]:
				animation = pyglet.image.load_animation(filename)
				frames = pyglet.image.atlas.TextureBin()
				animation.add_to_texture_bin(frames)
				self.current = pyglet.sprite.Sprite(animation)
			else:
				image = pyglet.image.load(filename)
				self.current = pyglet.sprite.Sprite(image)
		self.set_caption(filename)
		self.current.x = self.position[0]
		self.current.y = self.position[1]
		self.current.anchor_x = self.current.width // 2
		self.current.anchor_y = self.current.height // 2
		self.current.scale = self.scale

	def on_draw(self):
		self.clear()
		for sprite in self.placed:
			sprite.draw()
		self.current.draw()

	def on_key_press(self, symbol, modifier):
		if symbol in [48 + i for i in range(0, 10)]:
			self.current_index = (symbol - 48) % len(self.files)
			self.load()
		elif symbol == key.TAB:
			self.current_index = (self.current_index + 1) % len(self.files)
			self.load()
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
			self.load()
		elif symbol == key.RETURN:
			pyglet.image.get_buffer_manager().get_color_buffer().save('output.png')
		elif symbol == key.ESCAPE:
			self.clear()
			exit()


if __name__ == '__main__':
	win = Viewer('.' if len(sys.argv) < 2 else sys.argv[1])
	pyglet.app.run()

