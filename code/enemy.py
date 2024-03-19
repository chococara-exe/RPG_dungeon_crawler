import pygame, random
from settings import *
from entity import Entity
from support import *
from spriteSheet import SpriteSheet

class Enemy(Entity):
	'''this class is used to create an enemy that the player can attack. it will move towards the player if the player
	is in its notice radius. once the player is in its notice radius, the enemy will attack the player, which will
	reduce the health of the player. when the player attacks it, the enemy will lose health and when it dies, it will
	generate a random herb that will appear in the player's inventory'''

	def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player):
		super().__init__(groups)
		self.monster_name = monster_name
		self.import_graphics(monster_name)
		self.sprite_type = 'enemy'

		self.status = 'idle'
		self.image = self.idle_sheet.get_frame(0, 0, 32, 32, "black")

		self.rect = self.image.get_rect(center=pos)
		self.hitbox = self.rect.inflate(-110, -100)
		self.obstacle_sprites = obstacle_sprites

		#enemy information
		monster_info = monster_data[self.monster_name]
		self.health = monster_info['health']
		self.speed = monster_info['speed']
		self.attack_damage = monster_info['damage']
		self.resistance = monster_info['resistance']
		self.attack_radius = monster_info['attack_radius']
		self.notice_radius = monster_info['notice_radius']
		self.attack_type = monster_info['attack_type']

		#cooldowns
		self.can_attack = True
		self.attack_time = None
		self.attack_cooldown = 400
		self.damage_player = damage_player

		self.vulnerable = True
		self.hit_time = None
		self.invincibility_duration = 200

	def import_graphics(self, name):
		self.idle_sheet = SpriteSheet(f"../graphics/{name}/{name}_idle.png")
		self.move_sheet = SpriteSheet(f"../graphics/{name}/{name}_walk.png")
		self.hurt_sheet = SpriteSheet(f"../graphics/{name}/{name}_hurt.png")
		self.death_sheet = SpriteSheet(f"../graphics/{name}/{name}_death.png")
		self.animations = {'idle': self.idle_sheet.move(0, 4, 32, 32),
						   'attack': self.idle_sheet.move(3, 4, 32, 32),
						   'left': self.move_sheet.move(1, 4, 32, 32),
						   'right': self.move_sheet.move(2, 4, 32, 32),
						   'death': self.death_sheet.move(0, 4, 32, 32)
						   }


	def get_player_distance_direction(self, player):
		#gets the distance between the player and the enemy along with their direction
		enemy_vec = pygame.math.Vector2(self.rect.center)
		player_vec = pygame.math.Vector2(player.rect.center)
		distance = (player_vec - enemy_vec).magnitude()

		if distance > 0:
			direction = (player_vec - enemy_vec).normalize()
		else:
			direction = pygame.math.Vector2()

		return (distance, direction)

	def get_status(self, player):
		distance = self.get_player_distance_direction(player)[0]
		direction = self.get_player_distance_direction(player)[1]

		if distance <= self.attack_radius and self.can_attack:
			#attacks the player if the player is in the attack radius
			if self.status != 'attack':
				self.frame_index = 0
			self.status = 'attack'
		elif distance <= self.notice_radius:
			#moves towards the player if the player is in the notice radius
			if direction.x > 0:
				self.status = "right"
			else:
				self.status = "left"
		else:
			self.status = 'idle'

	def actions(self, player):
		#carries out what the enemy is supposed to be doing according to the status
		if self.status == 'attack':
			self.attack_time = pygame.time.get_ticks()
			self.damage_player(self.attack_damage)
		if self.status == "right" or self.status == "left":
			self.direction = self.get_player_distance_direction(player)[1]
		else:
			self.direction = pygame.math.Vector2()

	def animate(self):
		animation = self.animations[self.status]

		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			if self.status == 'attack':
				self.can_attack = False
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center=self.hitbox.center)

		#the enemy will flicker after it is attacked when it is immune to attacks
		if not self.vulnerable:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def cooldowns(self):
		#changes if the enemy can attack and if it is vulnerable if cooldown time has passed
		current_time = pygame.time.get_ticks()
		if not self.can_attack:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.can_attack = True

		if not self.vulnerable:
			if current_time - self.hit_time >= self.invincibility_duration:
				self.vulnerable = True

	def get_damage(self, player, attack_type):
		#when the player attacks, the enemy gets damaged if it is not immune
		if self.vulnerable:
			self.direction = self.get_player_distance_direction(player)[1]
			if attack_type == 'weapon':
				self.health -= player.get_full_weapon_damage()
			else:
				self.health -= player.get_full_magic_damage()
			self.hit_time = pygame.time.get_ticks()
			self.vulnerable = False

	def check_death(self):
		#checks if the enemy has died and adds an item to the player's inventory
		if self.health <= 0:
			self.kill()
			self.status = "death"
			reward = random.choice(list(herb_data.keys()))
			if reward in game_data[0]["inventory"]:
				game_data[0]["inventory"][reward] += 1
			else:
				game_data[0]["inventory"][reward] = 1

	def hit_reaction(self):
		#enables knockback on the enemy
		if not self.vulnerable:
			self.direction *= -self.resistance

	def update(self):
		self.hit_reaction()
		self.move(self.speed)
		self.animate()
		self.cooldowns()
		self.check_death()

	def enemy_update(self, player):
		self.get_status(player)
		self.actions(player)