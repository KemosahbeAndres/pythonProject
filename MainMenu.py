import pygame
import planes
import planes.gui
from colores import *
import owngui
import sys


class MainMenu(planes.gui.Container):
	def __init__(self, parent_rect):
		super().__init__('container_menu', 10, white)
		size = width, height = 400, 500
		btns_width, btns_height = 300, 60
		self.area = planes.Plane('area_menu', pygame.Rect((0, 0), size))
		self.area.image.fill(white)

		title = owngui.Header(
			'menu_title',
			'Menu Principal',
			pygame.Rect(((width / 2) - 100, 10), (200, 30)),
			white
		)
		self.area.sub(title)

		game_btn = planes.gui.Button('Nueva Partida',
									 pygame.Rect(((width / 2) - (btns_width / 2), title.image.get_height() + 40),
												 (btns_width, btns_height)), self.onClickNewGame)
		self.area.sub(game_btn)

		exit_btn = planes.gui.Button("Salir", pygame.Rect(
			((width / 2) - (btns_width / 2), title.image.get_height() + game_btn.image.get_height() + 50),
			(btns_width, btns_height)), self.onClickExit)
		self.area.sub(exit_btn)

		self.sub(self.area)
		self.rect.topleft = (parent_rect.centerx - (width / 2), 10)

		self.newGameListener = None

	def onClickNewGame(self, *args):
		if not self.newGameListener is None:
			self.newGameListener(1)

	def setNewGameListener(self, listener=None):
		if not listener is None:
			self.newGameListener = listener

	def onClickExit(self, *args):
		sys.exit(0)
