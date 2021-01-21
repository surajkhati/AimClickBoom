import pygame, random, shelve
pygame.init()
pygame.mixer.init()
pygame.font.init()

screen_size = (800, 600)
health = 100
score  = 0
final_screen = pygame.display.set_mode(screen_size)
enemy_count  = 0

class ColorClass:
	def __init__(self):
		self.white = (255, 255, 255)
		self.black = (0, 0, 0)
		self.red = (255, 0, 0)
		self.yellow = (255, 255, 0)
		self.green = (0, 255, 0)
		self.blue = (0, 0, 255)
		self.grey = (100, 100, 100)

color = ColorClass()

class StarClass:
	def __init__(self):
		self.size = random.randint(1, 3)
		self.position_x = random.randint(0 - 100, screen_size[0])
		self.position_y = random.randint(0, screen_size[1])
		self.sprite = pygame.Rect(self.position_x, self.position_y, self.size, self.size)
		self.speed = random.randint(3, 10)
		self.color = random.choice((color.white, color.grey))

	def draw(self, sprite):
		pygame.draw.rect(final_screen, self.color, sprite)

	def update(self):
		if self.position_x >= screen_size[0] - graphics.border_size / 2:
			self.__init__()
		self.position_x += self.speed
		sprite = pygame.Rect(self.position_x, self.position_y, self.size, self.size)
		self.draw(sprite)

class PlanetClass:
	def __init__(self):
		self.size = random.randint(600, 800)
		self.position_x = 0 - self.size - 1
		self.position_y = random.randint(0, screen_size[1] - int(self.size / 2))
		self.speed = random.randint(3, 5)

	def draw(self):
		self.image = pygame.transform.scale(graphics.planet_sprite, (self.size, self.size))
		final_screen.blit(self.image, (self.position_x, self.position_y))

	def update(self):
		if enemy_count == 50 and self.position_x >= screen_size[0]:
			self.__init__()
		self.position_x += self.speed
		self.draw()

class GraphicsClass:
	def __init__(self):
		# Border
		self.border_color = color.blue
		self.border_size  = 20
		self.border = (0, 0, screen_size[0] - 1, screen_size[1] - 1)

		# Fonts
		self.font_size = 32
		self.score_font = pygame.font.Font('nullp.ttf', self.font_size)
		self.text_surface = None

		# Stars

		self.stars = []
		for i in range(400):
			self.stars.append(StarClass())

		self.planet = PlanetClass()

		# Sprites
		self.asteroid_sprite = pygame.image.load('asteroid.png').convert_alpha()
		self.health_sprite = pygame.image.load('health.png').convert_alpha()
		self.planet_sprite = pygame.image.load('green_planet.png').convert_alpha()


	def draw_boundary(self):
		pygame.draw.rect(final_screen, self.border_color, self.border, self.border_size)

	def draw_scoreandhealth(self):
		self.text_surface = self.score_font.render("Health: " + str(health), False, color.yellow)
		final_screen.blit(self.text_surface, ((self.border_size / 2) + 10, (self.border_size / 2 + 10)))
		self.text_surface = self.score_font.render("Score: " + str(score), False, color.yellow)
		final_screen.blit(self.text_surface, ((self.border_size / 2) + 10, (self.border_size / 2 + 15 + self.font_size)))
		# high_score_text = "High Score: " + str(high_score.value)
		# self.text_surface = self.score_font.render(high_score_text, False, color.yellow)
		# final_screen.blit(self.text_surface, (screen_size[0] - len(high_score_text) * self.font_size - self.border_size / 2 - 5, (self.border_size / 2 + 10)))

	def game_over(self):
		final_screen.fill(color.black)
		self.draw_boundary()

		text = self.score_font.render('Game Over!', 1, color.red)
		text_rect = text.get_rect(center = (screen_size[0] // 2, screen_size[1] // 2))
		final_screen.blit(text, text_rect)
		pygame.display.update()

		pygame.time.delay(3000)


	def draw_background(self):
		for star in self.stars:
			star.update()

		self.planet.update()
	

graphics = GraphicsClass()

class SoundClass:
	def __init__(self):
		self.shoot = pygame.mixer.Sound('shoot.wav')
		self.explosion = pygame.mixer.Sound('explosion.wav')
		self.health_up = pygame.mixer.Sound('health_up.wav')
		self.hurt = pygame.mixer.Sound('hurt.wav')

		# self.bg_music = pygame.mixer.music.load('bg_music.mp3')
		# pygame.mixer.music.play(-1, 0.0)
sounds = SoundClass()

class EnemyClass:
	def __init__(self):

		global enemy_count
		print(enemy_count)
		enemy_count += 1

		self.color = random.choice([color.green, color.red])

		if self.color == color.green:
			self.size = 50
			self.image = pygame.transform.scale(graphics.health_sprite, (self.size, self.size))
			self.image = pygame.transform.rotate(self.image, random.randint(-360, 360))

		else:
			self.size = random.randint(100, 150)
			self.image = pygame.transform.scale(graphics.asteroid_sprite, (self.size, self.size))
		
		# self.image = pygame.transform.rotate(self.image, random.randint(-360, 360))
		self.speed_x = 10 #random.randint(15, 25)
		self.position_x = 0 - self.size
		self.position_y = random.randint(graphics.border_size / 2, screen_size[1] - self.size - graphics.border_size / 2)

		# self.sprite = pygame.Rect(self.position_x, self.position_y, self.size, self.size)

	def draw(self):
		# graphics.blit_alpha(final_screen, graphics.enemy_sprite, (self.position_x, self.position_y), 256)
		final_screen.blit(self.image, (self.position_x, self.position_y))
		pygame.draw.rect(final_screen, self.color, (self.position_x - 2, self.position_y - 2, self.size + 2, self.size + 2), 2)

	def update(self):
		global health, score, enemy_count
		if enemy_count == 50:
			enemy_count = 0
		if self.position_x >= screen_size[0]:

			if self.color == color.red:
				health -= 10
				sounds.hurt.play()
				final_screen.fill(color.red)
				graphics.draw_boundary()
				pygame.display.update()
				pygame.time.delay(200)

			self.__init__()

		self.position_x += self.speed_x
		self.sprite = pygame.Rect(self.position_x, self.position_y, self.size, self.size)

		self.draw()

	def confirm_shot(self, posx, posy):
		global score, health
		if posx >= self.position_x - self.size and posx <= self.position_x + self.size + self.size:
			if posy >= self.position_y - self.size and posy <= self.position_y + self.size + self.size:
				if self.color == color.red:
					sounds.explosion.play()
					score += 10
				else:
					sounds.health_up.play()
					if health >= 100:
						health = 100
					else:
						health += 10
				final_screen.fill(color.white)
				graphics.draw_boundary()
				pygame.display.update()
				self.__init__()
				return True
'''
	def auto_aim(self):
		global game
		game.player.position_x = self.position_x + self.size / 2
		game.player.position_y = self.position_y + self.size / 2
'''

class PlayerClass:
	def __init__(self):
		self.position_x = 40
		self.position_y = 40
		self.size = 20

	def draw(self, sprite):
		pygame.draw.circle(final_screen, color.white, sprite, self.size, 2)
		pygame.draw.line(final_screen, color.white, (sprite[0], sprite[1] - self.size - 5), (sprite[0], sprite[1] + self.size - 1 + 5), 2)
		pygame.draw.line(final_screen, color.white, (sprite[0] - self.size - 5, sprite[1]), (sprite[0] + self.size - 1 + 5, sprite[1]), 2)


	def update(self):
		self.position_x, self.position_y = pygame.mouse.get_pos()
		self.sprite = (self.position_x, self.position_y)

		self.draw(self.sprite)

class GameClass:
	def __init__(self):
		self.running = True
		self.game_over = False
		self.final_screen = None

		self.player = PlayerClass()
		self.enemy = EnemyClass()
		self.clock = pygame.time.Clock()

	def on_init(self):
		pygame.init()
		# load_highscore()
		pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
		pygame.display.set_caption("Shooter")

	def draw_screen(self):
		final_screen.fill(color.black)

		# Draw background
		graphics.draw_background()

		# Draw and update enemy
		self.enemy.update()

		# Draw and update player
		self.player.update()
		
		# Draw Boundary
		graphics.draw_boundary()

		# Display score here
		graphics.draw_scoreandhealth()
		# graphics.draw_score()

		pygame.display.flip()
		pygame.display.update()

	def check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					self.running = False
				elif event.key == pygame.K_r:
					global score, health
					score = 0
					health = 100
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					sounds.shoot.play()
					if self.enemy.confirm_shot(*pygame.mouse.get_pos()):
						print("Score: " + str(score))
						self.player.update()
						pygame.display.update()
						pygame.time.delay(100)

	def update(self):

		global health
		global score
		if health <= 0:
			graphics.game_over()
			health = 100
			score = 0

		if score <= 0:
			score = 0

		self.draw_screen()

	def run_game(self):
		self.on_init()

		while self.running:
			self.check_events()
			self.update()
			self.clock.tick(60)

game = GameClass()

def main():
	game.run_game()
	pygame.mixer.music.stop()
	pygame.quit()

main()
