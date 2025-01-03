import random
from tkinter import messagebox
import turtle
import pygame #sesleri eklmeke için kullandım
#mixeri aç
pygame.mixer.init() 

#ses dosyaları
explosion_sound = pygame.mixer.Sound("explosion.mp3")
hyperspace_sound = pygame.mixer.Sound("hyperspace.mp3")
laser_sound = pygame.mixer.Sound("laser_V2.mp3")
missile_sound = pygame.mixer.Sound("missile.mp3")
menu_music = pygame.mixer.Sound("menu_intro.mp3")
menu_music.play(1)
menu_music.set_volume(0.1) #sesi kıstım



def start_game1():
	def play_explosion_sound():
		explosion_sound.play()
		
	def play_hyperspace_sound():
		hyperspace_sound.play()

	def play_laser_sound():
		laser_sound.play()
		

	def play_missile_sound():
		missile_sound.play()
	#Required on Mac to create turtle window
	turtle.fd(0)
	#Max animation speed
	turtle.speed(10)
	#Change the background color of the screen
	turtle.bgcolor("black")
	#Load the background image
	turtle.bgpic("menu_V3.png")
	#Hide the turtle
	turtle.ht()
	#Set the undo buffer to 1 (to save memory and speed things up)
	turtle.setundobuffer(1)
	#Speed up drawing (Draw every 6 frames)
	turtle.tracer(2)  # Reduce the speed of drawing


	class Sprite(turtle.Turtle):
		def __init__(self, spriteshape, color, startx, starty):
			turtle.Turtle.__init__(self, shape = spriteshape)
			# self.speed(10) #speed of animasyooon
			self.penup()
			self.color(color)
			# self.fd(0) #for mac
			self.goto(startx, starty)
			self.speed = 5  # Reduce the speed of the sprite
			
		def is_collision(self, other):
			if (self.xcor() >= (other.xcor() - 20)) and \
				(self.xcor() <= (other.xcor() + 20)) and \
				(self.ycor() >= (other.ycor() - 20)) and \
				(self.ycor() <= (other.ycor() + 20)):
				return True
			else:
				return False
				
		def move(self):
			self.fd(self.speed)
			
			if self.xcor() < -290:
				self.rt(60)
				self.setx(-290)
			
			elif self.xcor() > 290:
				self.rt(60)
				self.setx(290)
				
			if self.ycor() < -290:
				self.rt(60)
				self.sety(-290)		
			
			elif self.ycor() > 290:
				self.rt(60)
				self.sety(290)

	class Player(Sprite):
		def __init__(self, spriteshape, color, startx, starty):
			Sprite.__init__(self, spriteshape, color, startx, starty)
			self.speed = 0
			self.health = 4
			self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
			
		def turn_left(self):
			self.lt(45)
			
		def turn_right(self):
			self.rt(45)
					
		def accelerate(self):
			self.speed += 1
			
		def decelerate(self):
			if self.speed > 0 :
				self.speed -= 1

			
		def hyperspace(self):
			play_hyperspace_sound()
			x = random.randint(-250, 250)
			y = random.randint(-250, 250)
			self.goto(x, y)
			self.setheading(random.randint(0,360))
			self.speed *= 0.5
			
	class Enemy(Sprite):
		def __init__(self, spriteshape, color, startx, starty):
			Sprite.__init__(self, spriteshape, color, startx, starty)
			self.speed = 0.5  # Further reduce the speed of the enemy
			self.setheading(random.randint(0,360))
			degrees = random.randint(20, 60)
			if self.xcor() < -290:
				self.rt(degrees)
				self.setx(-290)
			
			elif self.xcor() > 290:
				self.rt(degrees)
				self.setx(290)
				
			if self.ycor() < -290:
				self.rt(degrees)
				self.sety(-290)		
			
			elif self.ycor() > 290:
				self.rt(degrees)
				self.sety(290)

		def reset_position(self):
			self.goto(random.randint(-200, 200), random.randint(-200, 200))
			self.color("red")

	class Ally(Sprite):
		def __init__(self, spriteshape, color, startx, starty):
			Sprite.__init__(self, spriteshape, color, startx, starty)
			self.speed = 0.2  # Further reduce the speed of the ally
			self.setheading(random.randint(0,360))
			
		def move(self):
			self.fd(self.speed) #otomatik olarak atanması için koyduk
			
			degrees = random.randint(20, 60)
			
			if self.xcor() < -290:
				self.lt(degrees)
				self.setx(-290)
			
			elif self.xcor() > 290:
				self.lt(degrees)
				self.setx(290)
				
			if self.ycor() < -290:
				self.lt(degrees)
				self.sety(-290)		
			
			elif self.ycor() > 290:
				self.lt(degrees)
				self.sety(290)
				
		def avoid(self, other):
			if (self.xcor() >= (other.xcor() -40)) and \
				(self.xcor() <= (other.xcor() + 40)) and \
				(self.ycor() >= (other.ycor() -40)) and \
				(self.ycor() <= (other.ycor() + 40)):	
				self.lt(30)	


	class Bullet(Sprite):
		def __init__(self, spriteshape, color, startx, starty):
			Sprite.__init__(self, spriteshape, color, startx, starty)
			self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline=None)
			self.status = "ready"
			self.speed = 10  # Reduce the speed of the bullet
			
		def fire(self):
			if self.status == "ready":
				self.status = "shoot"
				play_laser_sound()
			
		def move(self):
			if self.status == "ready":
				self.hideturtle()
				#Move the turtle offscreen
				self.goto(-1000	,1000)
			
			if self.status == "shoot":
				self.goto(player.xcor(), player.ycor())
				self.setheading(player.heading())
				self.showturtle()
				self.status = "firing"
			
			if self.status == "firing":
				self.fd(self.speed)
				
			
			#Border Check	
			if self.xcor() < -290 or self.xcor() > 290 \
				or self.ycor() < -290 or self.ycor() > 290:
				self.status = "ready"			
				
	class Particle(Sprite):
		def __init__(self, spriteshape, color, startx, starty):
			Sprite.__init__(self, spriteshape, color, -1000, -1000)
			self.frame = 0
			self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
			
		def explode(self, startx, starty):
			turtle.tracer(8)
			self.goto(startx, starty)
			self.setheading(random.randint(0, 360))
			self.frame = 1

			
		def move(self):
			if self.frame != 0:
				self.fd(18-self.frame)
				self.frame += 1
				
				if self.frame < 6:
					self.shapesize(stretch_wid=0.3, stretch_len=0.3, outline=None)
				elif self.frame < 11:
					self.shapesize(stretch_wid=0.2, stretch_len=0.2, outline=None)
				else:
					self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
				
				if self.frame > 18:
					self.frame = 0
					self.goto(-1000, -1000)
					turtle.tracer(6)
							
	class Game():
		def __init__(self):
			self.level = 1
			self.score = 0
			self.state = "splash"
			self.pen = turtle.Turtle()
			self.health = 4
			self.level_thresholds = [400, 800, 1200, 2000]
			self.enemies = []
			
		def draw_border(self):
			#Draw Border
			self.pen.speed(0)
			self.pen.color("white")
			self.pen.pensize(3)
			self.pen.penup()
			self.pen.goto(-300, 300)
			self.pen.pendown()
			for side in range(4):
				self.pen.fd(600)
				self.pen.rt(90)
			self.pen.penup()
			
		def show_status(self):
			self.pen.undo()
			if game.health > 0:
				msg = "Level: %s Health: %s Score: %s " %(self.level, self.health, self.score)		
			else: 
				msg = "Game Over Score: %s" %(self.score)
			self.pen.penup()
			self.pen.goto(-300, 310)
			self.pen.write(msg, font=("Arial", 16, "normal"))

		def check_level_up(self):
			if self.level < len(self.level_thresholds) and self.score >= self.level_thresholds[self.level - 1]:
				# Önceki leveldeki düşmanların rengini beyaz yap
				for enemy in self.enemies:
					enemy.color("gray")
				
				self.level += 1
				self.show_status()
				messagebox.showinfo("Level Up", f"Welcome to Level {self.level}!")
				self.add_enemies()  # Yeni levelde yeni düşmanları ekle
			if self.score >= 3000:
				self.state = "gameover"
				messagebox.showinfo("Congratulations!", "You have reached 3000 points and won the game!")

		def add_enemies(self):
			num_enemies = self.level * 3
			self.enemies = []
			for e in range(num_enemies):
				x = random.randint(-200, 200)
				y = random.randint(-200, 200)
				self.enemies.append(Enemy("circle", "red", x, y))

	#Create game object
	game = Game()

	#Draw the game border
	game.draw_border()

	#Show the level and score
	game.show_status()

	#Create player and enemy objects
	player = Player("triangle", "white", 0.0, 0.0)
	#enemy = Enemy("circle", "red", 100.0, 0.0)
	bullet = Bullet("triangle", "yellow", 0.0, 0.0)
	#ally = Ally("square", "blue", 100, 100)

	#klavye ataması
	turtle.onkey(player.turn_left, "Left")
	turtle.onkey(player.turn_right, "Right")
	turtle.onkey(player.accelerate, "Up")
	turtle.onkey(player.decelerate, "Down")
	turtle.onkey(bullet.fire, "space")
	turtle.listen()

	#Set up the game
	#Create lists for sprites
	#Add Enemies
	if game.state == "splash":
		game.add_enemies()  # Initialize enemies based on the level

		#Add Allies
		allies = []
		for a in range(6):
			x = random.randint(-200, 200)
			y = random.randint(-200, 200)
			allies.append(Ally("square", "blue", x, y))
			
		particles = []

		for p in range(2):
			particles.append(Particle("circle", "yellow", -1000, -1000))
		for p in range(2):
			particles.append(Particle("circle", "red", -1000, -1000))
		for p in range(2):
			particles.append(Particle("circle", "orange", -1000, -1000))

		game.state = "playing"

	while True:
		turtle.update()
		if game.state == "restart":
			game.health = 4
			game.score = 0
			player.speed = 0
			player.goto(0,0)
			player.setheading(0)

			game.add_enemies()  # Reinitialize enemies based on the level

			for ally in allies:
				ally.goto(random.randint(-200, 200), random.randint(-200, 200))	
			
			game.state = "playing"
		
		if game.state == "playing":
			player.move()
			bullet.move()
			game.check_level_up()  # Check if the player has leveled up or won the game
		
			for enemy in game.enemies:	
				enemy.move()

				#Check collisions
				if player.is_collision(enemy):
					play_explosion_sound()
					player.color("red")
					for particle in particles:
						particle.explode(enemy.xcor(), enemy.ycor())
					player.rt(random.randint(100, 200))
					enemy.reset_position()  # Reset enemy position and color
					game.health -= 1
					if game.health < 1:
						game.state = "gameover"
					game.show_status()
					player.color("white")
			
				if bullet.is_collision(enemy):
					play_explosion_sound()
					for particle in particles:
						particle.explode(enemy.xcor(), enemy.ycor())
						
					bullet.status = "ready"
					enemy.color("white")  # Change enemy color to white
					enemy.reset_position()  # Reset enemy position and color
					enemy.speed += 0.2
					game.score += 100
					game.show_status()
				
			for ally in allies:
				ally.move()
				
				#Avoid enemy
				for enemy in game.enemies:	
					ally.avoid(enemy)
				
				#Allies should avoid player as well	
				ally.avoid(player)
		
				#Check collisions
				if bullet.is_collision(ally):
					for particle in particles:
						particle.explode(ally.xcor(), ally.ycor())
					bullet.status = "ready"
					ally.goto(random.randint(-200, 200), random.randint(-200, 200))	
					game.score -= 50
					game.show_status()
					
		for particle in particles:
			particle.move()
					
		if game.state == "gameover":
			for i in range(360):
				player.rt(1) 
			
			if messagebox.askyesno("Game Over", "Play again?") == True:
				game.state = "restart"
			else:
				exit()





# - ANA MENÜ BAŞLANGICI -

# Menü ekranını oluştur
menu_screen = turtle.Screen()
menu_screen.title("Alt+F4")
menu_screen.bgcolor("black")
menu_screen.setup(width=600, height=600)

# Yazı stilini ayarla
font_title = ("Arial", 24, "bold")
font_options = ("Arial", 18, "normal")
font_small = ("Arial", 12, "normal")

# Başlık yazdır
title = turtle.Turtle()
title.color("white")
title.penup()
title.hideturtle()
title.goto(0, 200)
title.write("The Alt-F4", align="center", font=font_title)
title.goto(0, 150) 
title.write("Furkan Turan - Taha Mert Yıldız - Burak Can Şen", align="center", font=font_small)

# Menü seçeneklerini yazdır
option_1 = turtle.Turtle()
option_1.color("green")
option_1.penup()
option_1.hideturtle()
option_1.goto(0, 50)
option_1.write("1. Start Game", align="center", font=font_options)

option_2 = turtle.Turtle()
option_2.color("red")
option_2.penup()
option_2.hideturtle()
option_2.goto(0, 0)
option_2.write("2. Exit Game", align="center", font=font_options)

# Kullanıcı seçimi için fonksiyonlar
def start_game():
    title.clear()
    option_1.clear()
    option_2.clear()
    menu_screen.bgcolor("blue")
    
    start_game1()
    turtle.done()


def exit_game():
    menu_screen.bye()  # Turtle ekranını kapatır

# Kullanıcı etkileşimleri
menu_screen.listen()
menu_screen.onkey(start_game, "1")  # "1" tuşuna basıldığında oyunu başlatır
menu_screen.onkey(exit_game, "2")  # "2" tuşuna basıldığında oyundan çıkar

# Ekranı açık tut
menu_screen.mainloop()


# - ANA MENÜ BİTİŞİ -



