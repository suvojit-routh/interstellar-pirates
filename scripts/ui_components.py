import pygame

class Panel:
	def __init__(self, display, panel ,bg_element):
		self.display = display
		self.bg_element = bg_element
		self.display_width = self.display.get_width()
		self.display_height = self.display.get_height()

		# Panel size (90% of display area)
		self.width = int(self.display_width * 0.9)
		self.height = int(self.display_height * 0.9)

		# Position to center the panel
		self.x = (self.display_width - self.width) // 2
		self.y = (self.display_height - self.height) // 2

		# Create a surface with alpha support
		self.panel = panel

		# Header bar
		self.header_height = 50  # Height of the top bar

		# Font for title
		self.font = pygame.font.Font('font/subatomic.ttf', 40)

	def draw(self , header):
		# Draw background first
		self.bg_element.draw(self.display)
		self.bg_element.update()

		# Clear panel each frame
		self.panel.fill((0, 0, 0, 0))

		# --- Draw main panel background (glass effect) ---
		dark_glass = (20, 20, 20, 200)  # RGBA with transparency
		pygame.draw.rect(
		self.panel,
		dark_glass,
		(0, 0, self.width, self.height),
		border_radius=10
		)

		# --- Draw top header bar ---
		header_color = (0, 90, 200, 230)  # Semi-transparent blue
		pygame.draw.rect(
		self.panel,
		header_color,
		(0, 0, self.width, self.header_height),
		border_top_left_radius=10,
		border_top_right_radius=10
		)

		# --- Title text ---
		title_surface = self.font.render(f"{header}", True, (255, 255, 255))
		title_rect = title_surface.get_rect(center=(self.width // 2, self.header_height // 2))
		self.panel.blit(title_surface, title_rect)

		# --- Draw thin border around panel ---
		pygame.draw.rect(
		self.panel,
		(200, 200, 200, 150),
		(0, 0, self.width, self.height),
		width=1,
		border_radius=10
		)

		# Blit the completed panel onto the main display
		self.display.blit(self.panel, (self.x, self.y))

