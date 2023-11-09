import planes.gui
import pygame


class Header(planes.gui.Label):
	def __init__(self, name, text, rect, background_color=None, text_color=(0, 0, 0)):
		super().__init__(name, text, rect, background_color, text_color)

	def redraw(self):
		"""
		Redraw the Label if necessary.
		"""

		if self.text != self.cached_text or self.current_color != self.cached_color:
			self.image.fill(self.current_color)

			# Text is centered on rect.
			#
			fontsurf = planes.gui.BIG_FONT.render(self.text, True, self.text_color)

			centered_rect = fontsurf.get_rect()

			# Get a neutral center of self.rect
			#
			centered_rect.center = pygame.Rect((0, 0), self.rect.size).center

			self.image.blit(fontsurf, centered_rect)

			# Force redraw in render()
			#
			self.last_rect = None

			self.cached_text = self.text
			self.cached_color = self.current_color
		return


class OkBox(planes.gui.Container):
	"""A box which displays a message and an OK button.
	   It is destroyed when OK is clicked.
	   The message will be wrapped at newline characters.
	"""

	def __init__(self, message, listener=None):
		"""Initialise.
		"""
		# Base class __init__()
		# We need a unique random name an just use this instance's id.
		# TODO: prefix with some letters to make it usable via attribute calls
		#
		super().__init__(str(id(self)), 5)

		lines = message.split("\n")

		for line_no in range(len(lines)):

			self.sub(planes.gui.Label("message_line_{0}".format(line_no),
						   lines[line_no],
						   pygame.Rect((0, 0), (len(lines[line_no]) * planes.gui.PIX_PER_CHAR, 30))))

		self.sub(planes.gui.Button("OK", pygame.Rect((0, 0), (50, 30)), self.ok))
		self.listener = listener

	def ok(self, plane):
		"""Button clicked callback which destroys the OkBox.
		"""
		self.destroy()

		if not self.listener is None:
			self.listener()
