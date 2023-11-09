import pygame
import planes
import planes.gui
import owngui
import colores
import random


topleft = 1
topright = 2
bottomleft = 3
bottomright = 4
center = 5
left=6
right=7
top=8
bottom=9

class ScoreBoard(planes.Plane):
	def __init__(self, rect: pygame.Rect, lives=3, xp=0):
		super().__init__(
			'scoreboard',
			pygame.Rect(
				(0, 0),
				(rect.width, 40)
			)
		)
		self.lives_count = lives
		self.xp = xp

		self.lives_label = planes.gui.Label('lives_label', "Vidas: " + str(self.lives_count), pygame.Rect((6, 1), (80, 18)))
		self.xp_label = planes.gui.Label('experience_label', "XP: " + str(self.xp), pygame.Rect((self.lives_label.image.get_width() + 12, 1), (100, 18)))

		self.sub(self.lives_label)
		self.sub(self.xp_label)

	def update(self):
		super().update()
		self.lives_label.text = "Vidas: " + str(self.lives_count)
		self.xp_label.text = "XP: " + str(self.xp)

	def add_live(self, count=1):
		self.lives_count += int(count)
		if self.lives_count > 999:
			self.lives_count = 999

	def drop_live(self, count=1):
		self.lives_count -= int(count)
		if self.lives_count <= 0:
			self.lives_count = 0

	def add_xp(self, count=1):
		self.xp += int(count)
		if self.xp > 9999:
			self.xp = 9999

	def drop_xp(self, count=1):
		self.xp -= int(count)
		if self.xp <= 0:
			self.xp = 0

class Player(planes.Plane):
	def __init__(self, rect: pygame.Rect, width=100):
		super().__init__(
			'player',
			pygame.Rect(
				(rect.centerx-50, rect.height-80),
				(width, 6)
			)
		)
		self.image.fill(colores.white)
		self.velocity = 3
		self.direction = center

	def stop(self):
		self.velocity = 0

	def move(self, velocity=3):
		self.velocity = velocity

	def add_width(self, width=50):
		size = self.rect.width+width, self.rect.height
		self.rect.update(self.rect.topleft, size)

	def update(self):
		super().update()
		keys = pygame.key.get_pressed()
		last_position = self.rect.x
		if keys[pygame.K_LEFT]:
			self.rect.x -= self.velocity
			self.direction = left
		elif keys[pygame.K_RIGHT]:
			self.direction = right
			self.rect.x += self.velocity
		else:
			self.direction = center

		if self.rect.x <= 0:
			self.rect.x = 0
		elif (self.rect.x+self.rect.width) >= (self.parent.rect.x+self.parent.rect.width-self.rect.width):
			self.rect.x = last_position
class Ball(planes.Plane):
	def __init__(self, rect: pygame.Rect):
		super().__init__(
			'ball',
			pygame.Rect(
				(random.randint(20, rect.width-40), random.randint(10, rect.centery-20)),
				(10, 10)
			)
		)
		self.image.fill(colores.white)
		self.velocity = 0
		self.direction = random.randint(1,2)

	def update(self):
		super().update()
		x, y = self.rect.center
		if self.direction == bottomright:
			self.rect.center = x + self.velocity, y + self.velocity
		elif self.direction == bottomleft:
			self.rect.center = x - self.velocity, y + self.velocity
		elif self.direction == topright:
			self.rect.center = x + self.velocity, y - self.velocity
		elif self.direction == topleft:
			self.rect.center = x - self.velocity, y - self.velocity

	def stop(self):
		self.velocity = 0

	def move(self, velocity=4):
		self.velocity = velocity

	def topleft(self):
		self.direction = topleft

	def topright(self):
		self.direction = topright

	def bottomleft(self):
		self.direction = bottomleft

	def bottomright(self):
		self.direction = bottomright

	def top_collide(self):
		if self.direction == topleft:
			self.direction = bottomleft
		elif self.direction == topright:
			self.direction = bottomright

	def bottom_collide(self):
		if self.direction == bottomleft:
			self.direction = topleft
		elif self.direction == bottomright:
			self.direction = topright

	def left_collide(self):
		if self.direction == bottomleft:
			self.direction = bottomright
		elif self.direction == topleft:
			self.direction = topright

	def right_collide(self):
		if self.direction == bottomright:
			self.direction = bottomleft
		elif self.direction == topright:
			self.direction = topleft

	def player_collide(self, direction=center):
		if direction == left:
			self.direction = topleft
		elif direction == right:
			self.direction = topright
		else:
			self.bottom_collide()


class BallPlatformGame(planes.Plane):
	def __init__(self, rect: pygame.Rect, endGameListener=None):
		super().__init__(
			'ball_plataform_game',
			pygame.Rect(
				(rect.centerx - 300, rect.centery - 300),
				(600, 600)
			)
		)
		self.image.fill(colores.black)
		self.endGameListener = endGameListener

		self.scoreboard = ScoreBoard(self.image.get_rect())
		self.sub(self.scoreboard)

		self.board = planes.Plane(
			'board',
			pygame.Rect(
				(0, 30),
				(600, 600-30)
			)
		)

		self.ball = Ball(self.board.image.get_rect())
		self.board.sub(self.ball)
		self.sub(self.board)

		self.player = Player(self.image.get_rect())
		self.sub(self.player)
		self.level_one = False

	def setOnEndGameListener(self, listener=None):
		if not listener is None:
			self.endGameListener = listener

	def play(self):
		self.player.move()
		if self.level_one:
			self.ball.move(6)
		else:
			self.ball.move()
		point = self.ball.rect.centery+25, self.ball.rect.bottom+25
		line = (self.ball.rect.x+25, self.ball.rect.bottom+25), (self.ball.rect.right+25, self.ball.rect.bottom+25)

		if self.ball.rect.top <= self.board.rect.x:
			self.ball.top_collide()
			print("top collide")
		elif self.ball.rect.left <= self.board.rect.left:
			self.ball.left_collide()
			print("left collide")
		elif self.ball.rect.right >= self.board.rect.right:
			self.ball.right_collide()
			print("right collide")
		elif self.ball.rect.y >= self.board.rect.bottom-self.board.rect.top:
			self.ball.bottom_collide()
			print("bottom collide")
			self.scoreboard.drop_live()
			self.board.remove('ball')
			self.ball.destroy()
			self.ball = Ball(self.board.rect)
			self.board.sub(self.ball)
		elif self.player.rect.clipline(line):
			self.ball.player_collide(self.player.direction)
			self.scoreboard.add_xp(5)
			print("PLAYER collide")

		if self.scoreboard.xp >= 8 and not self.level_one:
			self.ball.move(8)
			self.player.add_width()
			self.level_one = True
			print("levelup", self.ball.velocity, self.player.rect.width)

		if self.scoreboard.lives_count <= 0:
			self.ball.stop()
			self.player.stop()
			toast = owngui.OkBox("GAME OVER!!", self.endGameListener)
			self.sub(toast)
