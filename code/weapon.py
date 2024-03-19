import pygame 

class Weapon(pygame.sprite.Sprite):

	'''this class is use to get the weapon image and display it on the screen. a weapon will be generated when the
	player does an attack'''

	def __init__(self, player, groups):
		super().__init__(groups)
		self.sprite_type = 'weapon'
		direction = player.status.split('_')[0]

		full_path = f'../graphics/weapons/{player.weapon}/{direction}.png'
		self.image = pygame.image.load(full_path).convert_alpha()

		#blits the weapon image in the direction that the player is facing
		if direction == 'right':
			self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(-45, 10))
		elif direction == 'left': 
			self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(45, 10))
		elif direction == 'down':
			self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10, -55))
		else:
			self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(10, 65))
