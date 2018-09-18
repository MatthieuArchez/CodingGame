import sys
import math

WIDTH  = 40
HEIGHT = 18

class Giant:
	def __init__(self, x, y):
		self._x = x
		self._y = y

class Thor:
	def __init__(self, tx, ty):
		self._x = tx
		self._y = ty
		self._strikes = 0
		self._endangered = False

	def update (self, remaining_strikes):
		self._strikes = remaining_strikes
		self._endangered = False

	def is_giant_nearby (self, giant):
		is_nearby = False
		if math.fabs((giant._x - self._x)) <= 4 and math.fabs((giant._y - self._y)) <= 4:
			is_nearby = True
		return is_nearby

	def is_thor_endangered (self, giant):
		if math.sqrt((self._x - giant._x)**2 + (self._y - giant._y)**2) < 2:
			self._endangered = True
		return self._endangered



# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

tx, ty = [int(i) for i in input().split()]
thor = Thor(tx, ty)
giants = []


# game loop
while True:
	# h: the remaining number of hammer strikes.
	# n: the number of giants which are still present on the map.
	remaining_strikes, nb_giants = [int(i) for i in input().split()]
	giants = []
	for i in range(nb_giants):
		x, y = [int(j) for j in input().split()]
		new_giant = Giant(x, y)
		giants.append(new_giant)

	thor.update(remaining_strikes)

	free_dir = ["N", "NE", "E" ,"SE", "S", "SW" ,"W", "NW"]

	# Write an action using print
	# To debug: print("Debug messages...", file=sys.stderr)
	for giant in giants:
		if not thor.is_thor_endangered (giant):
			if thor.is_giant_nearby(giant):
				if thor._x == giant._x:
					if thor._y > giant._y:
						if "N" in free_dir : free_dir.remove("N")
						if "NE" in free_dir : free_dir.remove("NE")
						if "NW" in free_dir : free_dir.remove("NW")
					else:
						if "S" in free_dir : free_dir.remove("S")
						if "SE" in free_dir : free_dir.remove("SE")
						if "SW" in free_dir : free_dir.remove("SW")
				elif thor._y == giant._y:
					if thor._x > giant._x:
						if "W" in free_dir : free_dir.remove("W")
						if "NW" in free_dir : free_dir.remove("NW")
						if "SW" in free_dir : free_dir.remove("SW")
					else:
						if "E" in free_dir : free_dir.remove("E")
						if "NE" in free_dir : free_dir.remove("NE")
						if "SE" in free_dir : free_dir.remove("SE")
				elif thor._x > giant._x and thor._y > giant._y:
					if "NW" in free_dir : free_dir.remove("NW")
					if "W" in free_dir : free_dir.remove("W")
					if "N" in free_dir : free_dir.remove("N")
				elif thor._x > giant._x and thor._y < giant._y:
					if "SW" in free_dir : free_dir.remove("SW")
					if "W" in free_dir : free_dir.remove("W")
					if "S" in free_dir : free_dir.remove("S")
				elif thor._x < giant._x and thor._y > giant._y:
					if "NE" in free_dir : free_dir.remove("NE")
					if "E" in free_dir : free_dir.remove("E")
					if "N" in free_dir : free_dir.remove("N")
				elif thor._x < giant._x and thor._y < giant._y:
					if "SE" in free_dir : free_dir.remove("SE")
					if "E" in free_dir : free_dir.remove("E")
					if "S" in free_dir : free_dir.remove("S")

	if thor._x == WIDTH - 1:
		if "E" in free_dir : free_dir.remove("E")
		if "NE" in free_dir : free_dir.remove("NE")
		if "SE" in free_dir : free_dir.remove("SE")
	elif thor._x == 0:
		if "W" in free_dir : free_dir.remove("W")
		if "NW" in free_dir : free_dir.remove("NW")
		if "SW" in free_dir : free_dir.remove("SW")
	if thor._y == HEIGHT - 1:
		if "S" in free_dir : free_dir.remove("S")
		if "SE" in free_dir : free_dir.remove("SE")
		if "SW" in free_dir : free_dir.remove("SW")
	elif thor._y == 0:
		if "N" in free_dir : free_dir.remove("N")
		if "NE" in free_dir : free_dir.remove("NE")
		if "NW" in free_dir : free_dir.remove("NW")

	if thor._endangered:
		thor._strikes -= 1
		print ("STRIKE")
	elif len (free_dir) > 0:
		safe_dir = free_dir.pop()
		if safe_dir == "N":
			thor._y -= 1
		elif safe_dir == "S":
			thor._y += 1
		elif safe_dir == "W":
			thor._x -= 1
		elif safe_dir == "E":
			thor._x += 1
		elif safe_dir == "NW":
			thor._x -= 1
			thor._y -= 1
		elif safe_dir == "SW":
			thor._x -= 1
			thor._y += 1
		elif safe_dir == "NE":
			thor._x += 1
			thor._y -= 1
		elif safe_dir == "SE":
			thor._x += 1
			thor._y += 1

		print (safe_dir)
	else:
		# Let dem come
		print ("WAIT")
