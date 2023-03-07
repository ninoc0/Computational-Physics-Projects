import pygame
import math
pygame.init()

WIDTH, HEIGHT =  1000, 1000 # change window size
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

YELLOW = (253, 184, 19)
BLUE = (107, 147, 214)

class PBody:
	AU = 149.6e6 * 1000 # astronmical units
	G = 6.67428e-11 # gravity
	SCALE = 250 / AU  # 1AU = 100 pixels, this changes the speed of the animation
	TIME = 3600 * 24

	def __init__(self, x, y, radius, color, mass):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.mass = mass

		self.orbit = []
		self.sun = False # since the sun is a different planetary body
		self.distance = 0 

		self.x_vel = 0
		self.y_vel = 0

	def draw(self, win):
		x = self.x * self.SCALE + WIDTH / 2 # origin is originally in the corner for some reason so i fixed that
		y = self.y * self.SCALE + HEIGHT / 2 # sets origin for each planetary body

		if len(self.orbit) > 2: #this is just to create a trail
			updated_points = []
			for point in self.orbit:
				x, y = point
				x = x * self.SCALE + WIDTH/2
				y = y * self.SCALE + HEIGHT/2
				updated_points.append((x,y))

			pygame.draw.lines(win, self.color, False, updated_points, 2)

		pygame.draw.circle(win, self.color, (x, y), self.radius)

	def g_attraction(self, new):
		new_x, new_y = new.x, new.y # new x and self x are just x and x_1
		distance_x = new_x - self.x
		distance_y = new_y - self.y
		distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

		if new.sun:
			self.distance_to_sun = distance # put sun at origin

		force = self.G * self.mass * new.mass / distance**2
		theta = math.atan2(distance_y, distance_x)
		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force
		return force_x, force_y

	def update_position(self, planets):
		total_fx = total_fy = 0
		for planet in planets:
			if self == planet:
				continue

			fx, fy = self.g_attraction(planet)
			total_fx += fx
			total_fy += fy

		self.x_vel += total_fx / self.mass * self.TIME
		self.y_vel += total_fy / self.mass * self.TIME

		self.x += self.x_vel * self.TIME
		self.y += self.y_vel * self.TIME
		self.orbit.append((self.x, self.y)) #constantly updates the position


def main():
	run = True
	clock = pygame.time.Clock()

	sun = PBody(0, 0, 109, YELLOW, 1.98892 * 10**30)
	sun.sun = True

	earth = PBody(1* PBody.AU, 0, 1, BLUE, 5.9743 * 10**24)
	earth.y_vel = 29.783 * 1000


	planets = [sun, earth]

	while run:
		clock.tick(60) # speed up or slow down orbit 60
		WIN.fill((0, 0, 0)) # set the background color

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		for planet in planets:
			planet.update_position(planets)
			planet.draw(WIN)

		pygame.display.update()

	pygame.quit()


main()