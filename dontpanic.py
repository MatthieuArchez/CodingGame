import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# nb_floors: number of floors
# width: width of the area
# nb_rounds: maximum number of rounds
# exit_floor: floor on which the exit is found
# exit_leading_pos: position of the exit on its floor
# nb_total_clones: number of generated clones
# nb_additional_elevators: ignore (always zero)
# nb_elevators: number of elevators
class field:
    def __init__(self, width, nb_floors, nb_elevators, exit_floor, exit_leading_pos, nb_additional_elevators):
        self._width = width
        self._nb_floors = nb_floors
        self._nb_elevators = nb_elevators
        self._nb_additional_elevators = nb_additional_elevators
        self._exit_floor = exit_floor
        self._exit_leading_pos = exit_leading_pos
        self._elevators = {}
        
    def fill_elevator (self, elevator_floor, elevator_leading_pos):
        self._elevators[elevator_floor].append(elevator_leading_pos)
        
class clone:
    def __init__(self, nb_clones, pos, floor, direction, nb_additional_elevators):
        self._nb_total_clones = nb_clones
        self._nb_remaining_clones = nb_clones
        self._nb_remaining_elevators = nb_additional_elevators
        self._leading_pos = pos
        self._floor = floor
        self._direction = direction
        
    def update (self, pos, floor, direction):
        self._leading_pos = pos
        self._leading_floor = floor
        self._direction = direction
        
        
nb_floors, width, nb_rounds, exit_floor, exit_leading_pos, nb_total_clones, nb_additional_elevators, nb_elevators = [int(i) for i in input().split()]
print ("NB floors : " + str(nb_floors), file=sys.stderr)
print ("NB rounds : " + str(nb_floors), file=sys.stderr)
print ("NB elevators : " + str(nb_elevators), file=sys.stderr)
print ("Exit floor : " + str(exit_floor), file=sys.stderr)
print ("NB add elevators : " + str (nb_additional_elevators), file=sys.stderr)

level_field = field (width, nb_floors, nb_elevators, exit_floor, exit_leading_pos, nb_additional_elevators)

marvin = clone (nb_total_clones, 0, 0, "RIGHT", nb_additional_elevators)

for i in range(nb_floors):
    level_field._elevators[i] = []

for i in range(nb_elevators):
    # elevator_floor: floor on which this elevator is found
    # elevator_leading_pos: position of the elevator on its floor
    elevator_floor, elevator_leading_pos = [int(j) for j in input().split()]
    level_field.fill_elevator (elevator_floor, elevator_leading_pos)

print (level_field._elevators, file=sys.stderr)

# game loop
while True:
    # clone_floor: floor of the leading clone
    # clone_leading_pos: position of the leading clone on its floor
    # direction: direction of the leading clone: LEFT or RIGHT
    clone_floor, clone_leading_pos, direction = input().split()
    clone_floor = int(clone_floor)
    clone_leading_pos = int(clone_leading_pos)
    
    marvin.update(clone_leading_pos, clone_floor, direction)

    # If no clone available, do nothing
    if clone_floor == -1:
        print ("WAIT")
    # If Marvin on exit floor, block to change direction or continue
    elif marvin._leading_floor == level_field._exit_floor:
        if (marvin._leading_pos > level_field._exit_leading_pos and marvin._direction == "RIGHT") or (marvin._leading_pos < level_field._exit_leading_pos and marvin._direction == "LEFT"):
            print("BLOCK")
        else:
            print ("WAIT")
    # If Marvin on a floor with elevator, find the closest one, block or continue
    elif marvin._leading_floor in level_field._elevators and len (level_field._elevators[marvin._leading_floor]) > 0:
        min_dist = level_field._width + 1
        for elevator_pos in level_field._elevators[marvin._leading_floor]:
            dist = abs (marvin._leading_pos - elevator_pos)
            if dist < min_dist:
                closest_elevator_pos = elevator_pos
                min_dist = dist
        if (marvin._leading_pos > closest_elevator_pos and marvin._direction == "RIGHT") or (marvin._leading_pos < closest_elevator_pos and marvin._direction == "LEFT"):
            print ("BLOCK")
        else:
            print ("WAIT")
    # If marvin has no elevator, create one
    else:
        # Build elevator
        level_field._elevators[marvin._leading_floor].append(marvin._leading_pos)
        marvin._nb_remaining_elevators -= 1
        print ("ELEVATOR")


