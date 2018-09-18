import sys
import math
import queue

class field:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._laby = {}
        self._nb_entity = 0
    
    def build_laby (self, line, nb_line):
        counter = 0
        for elem in list(line):
            self._laby [counter, nb_line] = elem
            counter+=1


class explorer:
    def __init__(self, x, y , id, sanity):
        self._x = x
        self._y = y
        self._sanity = sanity
        self._id = id
        
        self._remaining_turns_light = 0
        self._torch = "Off"
        self._nb_torchs = 3
        
        self._remaining_turns_plan = 0
        self._plan = "Off"
        self._nb_plans = 3
        
    def update (self, x, y, id, sanity):
        self._x = x
        self._y = y
        self._sanity = sanity
        self._id = id

        if self._torch == "On":
            self._remaining_turns_light -= 1
        if self._remaining_turns_light <= 0:
            self._torch = "Off"

        if self._plan == "On":
            self._remaining_turns_plan -= 1
        if self._remaining_turns_plan <= 0:
            self._plan = "Off"

    def light_torch (self):
        self._torch = "On"
        self._remaining_turns_light = 3
        self._nb_torchs -= 1

    def start_planning (self):
        self._remaining_turns_plan = 5
        self._nb_plans -= 1
        self._plan = "On"
        
        
        
class wanderer:
    def __init__ (self, x, y, id, target_id, state, time):
        self._x = x
        self._y = y
        self._id = id
        self._target_id = target_id
        self._state = state
        self._time = time
        
    def update(self, x, y, target_id, state, time):
        self._x = x
        self._y = y
        self._target_id = target_id
        self._state = state
        self._time = time



def calculate_nb_moves (x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    
    
def calculate_points (x, y):
    
    min = 10000
    if len(wanderers) > 0:
        for elem in wanderers:
            temp = calculate_nb_moves(x, y, elem._x, elem._y)
            if temp < min:
                min = temp
                closest_wanderer = elem
    else:
        return 0
    
    return calculate_nb_moves (x, y, closest_wanderer._x, closest_wanderer._y)
    
        

# Build game field
mugu_the_explorer = explorer (0, 0, 0, 0)
wanderers = []
explorers = []
possible_tiles = []


game_field = field (int(input()), int(input()))
for i in range(game_field._height):
    game_field.build_laby (input(), i)
    
# sanity_loss_lonely: how much sanity you lose every turn when alone, always 3 until wood 1
# sanity_loss_group: how much sanity you lose every turn when near another player, always 1 until wood 1
# wanderer_spawn_time: how many turns the wanderer take to spawn, always 3 until wood 1
# wanderer_life_time: how many turns the wanderer is on map after spawning, always 40 until wood 1

sanity_loss_lonely, sanity_loss_group, wanderer_spawn_time, wanderer_life_time = [int(i) for i in input().split()]

# game loop
while True:
    field._entity_count = int(input())  # the first given entity corresponds to your explorer
    
    # Update my own explorer
    entity_type, id, x, y, param_0, param_1, param_2 = input().split()
    id = int(id)
    x = int(x)
    y = int(y)
    param_0 = int(param_0)
    param_1 = int(param_1)
    param_2 = int(param_2)
    mugu_the_explorer.update (x, y, id, param_0)
    
    # update others
    for i in range(field._entity_count - 1):
        entity_type, id, x, y, param_0, param_1, param_2 = input().split()
        id = int(id)
        x = int(x)
        y = int(y)
        param_0 = int(param_0)
        param_1 = int(param_1)
        param_2 = int(param_2)
        
        if entity_type == "EXPLORER":
            found = False
            for elem in explorers:
                if elem._id == id:
                    elem.update (x, y, id, param_0)
                    found = True
            if not found:
                explorers.append (explorer(x, y, id, param_0))
        elif entity_type == "WANDERER":
            found = False
            for elem in wanderers:
                if elem._id == id:
                    elem.update (x, y, param_0, param_1, param_2)
                    found = True
            if not found:
                wanderers.append (wanderer(x, y, id, param_0, param_1, param_2))
        
    
    # Determine which of the adjacent tiles are suitable for a move
    # Get the type of the adjacent tiles
    del possible_tiles [:] # Flush previous
   
    if (mugu_the_explorer._x, mugu_the_explorer._y + 1) in game_field._laby:
        if game_field._laby[mugu_the_explorer._x, mugu_the_explorer._y + 1] == "." or game_field._laby[mugu_the_explorer._x, mugu_the_explorer._y + 1] == "w":
            possible_tiles.append ((calculate_points (mugu_the_explorer._x, mugu_the_explorer._y + 1), mugu_the_explorer._x, mugu_the_explorer._y + 1))
    if (mugu_the_explorer._x + 1, mugu_the_explorer._y) in game_field._laby:
        if game_field._laby[mugu_the_explorer._x + 1, mugu_the_explorer._y] == "." or game_field._laby[mugu_the_explorer._x + 1, mugu_the_explorer._y] == "w":
            possible_tiles.append ((calculate_points (mugu_the_explorer._x + 1, mugu_the_explorer._y), mugu_the_explorer._x + 1, mugu_the_explorer._y))
    if (mugu_the_explorer._x - 1, mugu_the_explorer._y) in game_field._laby:
        if game_field._laby[mugu_the_explorer._x - 1, mugu_the_explorer._y] == "." or game_field._laby[mugu_the_explorer._x - 1, mugu_the_explorer._y] == "w":
            possible_tiles.append ((calculate_points (mugu_the_explorer._x - 1, mugu_the_explorer._y), mugu_the_explorer._x - 1, mugu_the_explorer._y))
    if (mugu_the_explorer._x, mugu_the_explorer._y - 1) in game_field._laby:
        if game_field._laby[mugu_the_explorer._x, mugu_the_explorer._y - 1] == "." or game_field._laby[mugu_the_explorer._x, mugu_the_explorer._y - 1] == "w":
            possible_tiles.append ((calculate_points (mugu_the_explorer._x, mugu_the_explorer._y - 1), mugu_the_explorer._x, mugu_the_explorer._y - 1))
    
    for elem in wanderers:
        if (calculate_points (mugu_the_explorer._x, mugu_the_explorer._y + 1), (elem._x, elem._y)) in possible_tiles:
            possible_tiles.remove(calculate_points (mugu_the_explorer._x, mugu_the_explorer._y + 1), (elem._x, elem._y))
    
    pts, dest_x, dest_y = max(possible_tiles)


    
    if pts >= 4.0 and mugu_the_explorer._nb_plans > 0 and mugu_the_explorer._plan == "Off":
        mugu_the_explorer.start_planning()
        print ("PLAN")
    
    elif pts < 3.0 and mugu_the_explorer._nb_torchs > 0 and mugu_the_explorer._torch == "Off":
        mugu_the_explorer.light_torch()
        print ("LIGHT")
    else:
        print("MOVE " + str(dest_x) + " " + str(dest_y))
