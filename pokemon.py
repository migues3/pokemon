import pygame
import player

from button import Button



class Pokemon:
	def __init__(self):
		self._running = True
		self._pause = False
		self.keys = None
		self.player = None
		self._window = None
		self._mousex, self._mousey = (0,0)

		self.avatarcell = 0
		# self.avatar = None

	def start_menu(self):
		start = True

		# While user is in the start menu	
		while start:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					start = False
					self.quit() 

			self._window.fill((255, 255, 255))

			start_text = pygame.font.SysFont('Comic Sans MS', 100, bold=True)
			text_surface = start_text.render('Pokemon', True, (0, 0, 0))
			w, h = self._window.get_size()
			text_rect = text_surface.get_rect(center = (w / 2, h - (h - 200)))
			self._window.blit(text_surface, text_rect)

			# Buttons: New Game and Load Game
			new_game = Button(self._window, (100, 300, 100, 50), (0, 0, 0), 'New Game', 15, 'Comic Sans MS',
				              (255, 255, 255))
			load_game = Button(self._window, (400, 300, 100, 50), (0, 0, 0), 'Load Game', 15, 'Comic Sans MS',
							  (255, 255, 255))
			new_game.create()
			load_game.create()

			if new_game.clicked():
				start = False
				self.character_selection()

			if load_game.clicked():
				pass	

			pygame.display.update()
	
	def character_selection(self):
		selection = True

		# While the user is selecting their character
		while selection:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					selection = False
					self.quit()

			self._window.fill((255, 255, 255))

			character = pygame.image.load('backgrounds/character1/bd.png').convert_alpha()
			# Going to need this to calculate which character to get from the whole image aka which movement
			image_size = character.get_size()
			# We want the first character in the first row so row = 1 and col = 1
			character_width, character_height = image_size[0] / 4, image_size[1] / 1


			self._window.blit(character, (300, 300), (0, 0, character_width, character_height))

			pygame.display.update()

	def play(self):
		'''if the game is in the playing state'''
		# self.player.avatar(1) ## CHOSE THE AVATAR from 1 - 5, Can put somewhere else
		# self.avatar = pygame.image.load(self.player.path).convert_alpha() # 

		# do the calculations of where to get the sprite movements
		area = self.avatar.get_width(), self.avatar.get_height() # get the dimension of the entire image
		sprite_width, sprite_height = area[0]/self.player.sprite_col(), area[1]/self.player.sprite_row() 
		
		while self._running:
			# print("Game is running")

			if self.player._avatar <= 2:
				## since if we choose avatar 1, 2 then 
				## we are loading different pictures since movements are croped
				## to different pictures
				self.avatar = pygame.image.load(self.player.path).convert_alpha()

			pygame.time.delay(100)
			# Just checks to see if user clicked the "X" on the top
			# right of the window

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()
				if event.type == pygame.VIDEORESIZE:
					### NEED MORE WORK, MAKE SURE TO SEPARATE TO ANOTHER FILE

					self._window = pygame.display.set_mode((event.w, event.h),
															pygame.RESIZABLE)
					self.player.x = event.w // 2
					self.player.y = event.h // 2
				elif event.type == pygame.MOUSEBUTTONDOWN:
					print("Mouse detected in play state")
					# if the user pressed the mouse
					### Not sure if we need this during the play state
					### Maybe if we click on something, we can get it's information??
					### Not sure, but doesn't need this
					self.handle_mouse()
			self.handle_play_events()

			### make a draw class
			self._window.fill((0, 0, 0)) 
			
			
			self._window.blit(self.avatar, 
				(self.player.x, self.player.y), 
				(self.player.current_col()*sprite_width,self.player.current_row() * sprite_height, 
				sprite_width, sprite_height))
			
			pygame.display.update()
	# def handle_pause_key_events():

	def pause(self):
		''' the pause state brings up the settings.
			So far, the setting includes exit, save, Pokedex(?), 
			Pokemon, Personal info (badges,etc), bags (items)'''

		### PROBLEM SO FAR IS THAT WHEN WE EXIT PLAY STATE WITH X
		### PAUSE FUNCTION IS CALLED BEFORE IT EXIT. 
		### NOT A MAJOR PROBLEM BUT PAUSE SHOULDN'T BE CALLED AT ALL
		### PUT IF ELSE STATEMENTS
		print("self.pause: pause state")

		setting = pygame.image.load('backgrounds/settings.png')
		self._window.blit(setting, (50,100))
		while self._pause == True:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						'''
						if user pressed esc again, then exit
						pause state and resume the play state. The time wait prevent
						the game from registering the key too fast  
						'''
						self._pause = False
						self._running = True
						pygame.time.wait(250)
					elif event.key == pygame.K_DOWN:
						pass
					elif event.key == pygame.K_UP:
						pass
				if event.type == pygame.MOUSEBUTTONDOWN:
					### If we use mouse instead of keyboard
					### Checks to see the mouse click is within range of the option
					### make sure to draw the options
					self.handle_mouse()
					# pass 
			# self.handle_setting()
			pygame.display.update()

	def run(self):

		pygame.init()
		self._window = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
		self.player = player.Player(300, 300)
		pygame.display.set_caption('Pokemon') # Sets the window name 

		##---------------------------set up characters -----------------##
		## let player choose types of avatar
		self.start_menu()
		
		self.player.avatar(1) ## CHOSE THE AVATAR from 1 - 5, Can put somewhere else
		self.avatar = pygame.image.load(self.player.path).convert_alpha() # 
		##--------------------------------------------------------------##
		

		while not (self._running == False and self._pause == False):
			
			self.play()
			self.pause()


		pygame.quit()


	def quit(self):
		'''kills the game'''
		self._running = False
		self._pause = False

	def button(self, x_pos, y_pos, width, height, text):
		pass

	def handle_mouse (self):
		self._mousex, self._mousey = pygame.mouse.get_pos()
		print("mouse coordinate: x = ", self._mousex, " y = ", self._mousey)
		# print(self._mousex, self._mousey)



	def handle_play_events(self):
		# function to handle movements
		keys = pygame.key.get_pressed()
		
		'''
		player movements
		'''

		if keys[pygame.K_UP]:
			self.player.moveup()
		if keys[pygame.K_DOWN]:
			self.player.movedown()
		if keys[pygame.K_RIGHT]:
			self.player.moveright()
		if keys[pygame.K_LEFT]:
			self.player.moveleft()

		'''settings. Problem: holding any key shouldn't do anything'''
		
		if keys[pygame.K_LCTRL] and keys[pygame.K_s]:
			print("Save option")
			f = open("SAVED_GAME.txt", "w+")
			### created a txt file for saved game, what what should be saved??

			f.write("%s\n", self.player._avatar) # Save the avatar

		if keys[pygame.K_ESCAPE]:
			# If user press esc, then bring up the setting option
			self._pause = True
			self._running = False
	

		

if __name__ == '__main__':
	Pokemon().run()
	print("in main")
    
