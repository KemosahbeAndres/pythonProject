import pygame
import planes
import planes.gui

from MainMenu import MainMenu
from games.ballplatformgame import BallPlatformGame

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

# APP STATES
WAITING = 0
PLAYING = 1
RESUMING = 2
SURRENDER = 3


class App:
	def __init__(self):
		self.width, self.height = 800, 600
		self.display = planes.Display((self.width, self.height))
		self.screen = self.display.display
		self.screen.fill(white)

		self.rect = self.screen.get_rect()
		pygame.display.set_caption("Testing Planes Library")
		self.running = False
		self.framerate = 60
		self.clock = pygame.time.Clock()

		background = planes.Plane('background', pygame.Rect((0, 0), (self.width, self.height)))
		image = pygame.image.load("img/fondo.jpg")
		format = image.get_width() / image.get_height()
		image = pygame.transform.scale(image, ((self.height * format), self.height))
		dest = self.rect.centerx - (image.get_width() / 2), self.rect.centery - (image.get_height() / 2)
		background.image.blit(image, dest)
		self.display.sub(background)

		self.ballgame = BallPlatformGame(self.display.display.get_rect())
		self.ballgame.setOnEndGameListener(self.end_game)

		self.state = WAITING
		self.state_change = True
		self.wait_index = 0


	def click(self, *args):
		print("Click! args: {0}".format(args))
		pass

	def play(self, state_code=WAITING):
		self.state = state_code
		self.state_change = True

	def end_game(self):
		self.state = WAITING
		self.state_change = True
		self.ballgame = BallPlatformGame(self.display.rect, self.end_game)

	def menu_in(self, seconds):
		if self.state == PLAYING and self.wait_index >= (self.framerate * seconds):
			self.state = WAITING
			self.state_change = True
			self.wait_index = 0
		elif self.state == PLAYING:
			self.wait_index += 1

	def run(self):
		menu = MainMenu(self.display.display.get_rect())
		menu.setNewGameListener(self.play)

		ballgame = BallPlatformGame(self.display.display.get_rect())
		ballgame.setOnEndGameListener(self.end_game)
		self.running = True

		while self.running:
			events = pygame.event.get()

			for event in events:
				if event.type == pygame.QUIT:
					pygame.quit()
					raise SystemExit

			if self.state_change:
				if self.state == WAITING:
					self.display.remove('ball_plataform_game')
					self.display.sub(menu)
				elif self.state == PLAYING:
					self.display.remove('container_menu')
					self.display.sub(self.ballgame)
				self.state_change = False

			if self.state == PLAYING:
				self.ballgame.play()
			# self.menu_in(2)

			self.display.process(events)
			self.display.update()
			self.display.render()

			pygame.display.flip()

			# Slow down to framerate given
			#
			self.clock.tick(self.framerate)


if __name__ == "__main__":
	app = App()
	app.run()
