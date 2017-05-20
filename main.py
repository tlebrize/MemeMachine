import pyglet, sys
from resources.window import TkWindow
from resources.world import TkWorld
from resources.menu import TkMenu
from resources.MmM import MemeMachine

class MainMenu(TkMenu):

	def __init__(self, world):
		self.label = "Main Menu"
		self.menu_items = {
			"Memes !"	: self.start,
			"Quit"		: self.quit
		}
		super(MainMenu, self).__init__(world)

	def start(self):
		self.world.transition("memes")

	def about(self):
		self.world.transition("about")

	def quit(self):
		self._quit()


def main(files_directory):
	window = TkWindow(800, 600, visible=False, caption="TESTMENULOL", style="dialog")
	world = TkWorld(window)
	main = MainMenu(world)
	mmm = MemeMachine(world, files_directory)
	world.add_scenes({"main": main, "memes" : mmm})
	world.transition("main")
	pyglet.app.run()

if __name__ == "__main__":
	main('.' if len(sys.argv) < 2 else sys.argv[1])