import sys
import math
from enum import Enum

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class Player:
    def __init__(self, health, mana, size_deck, rune):
        self._health = health
        self._mana = mana
        self._size_deck = size_deck
        self._size_hand = 0
        self._rune = rune
        self._board = []
        

    def update(self, health, mana, size_deck, rune):
        self._health = health
        self._mana = mana
        self._size_deck = size_deck
        self._rune = rune

        self._board.clear()

class Mugu_player(Player):
    def __init__(self, health, mana, size_deck, rune):
        super(Mugu_player, self).__init__(health, mana, size_deck, rune)
        self._hand = []

    def update(self, health, mana, size_deck, rune):
        super(Mugu_player, self).update(health, mana, size_deck, rune)
        self._hand.clear()
        
    def summon_minion(self, card):
        if len(self._board) < 6:
            self._mana -= card._cost
            if "C" in card._abilities:
                self._board.append(card)
            return ("SUMMON " + str(card._instance_id) + ";")
        else:
            return ("")
        
    def use_green_item(self, card):
        self._mana -= card._cost
        target = sorted (self._board, key=Card.getRatio)[0]
        return ("USE " + str(card._instance_id) + " " + str(target._instance_id) + ";")
    
    def use_red_item(self, card, opp_board):
        self._mana -= card._cost
        target = sorted (opp_board, key=lambda c:Card.getTarget(c, card._defense))[0]
        target._defense += card._defense
        if target._defense + card._defense <= 0:
            opp_board.remove(target)
        return ("USE " + str(card._instance_id) + " " + str(target._instance_id) + ";")
    
    def use_blue_item(self, card, opp_board):
        # TODO
        self._mana -= card._cost
        return ("USE " + str(card._instance_id) + " -1;")
        

class Card:

    def __init__(self, card_id, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw):
        self._id = card_id
        self._instance_id = instance_id
        self._location = location
        self._card_type = card_type
        self._cost = cost
        self._attack = attack
        self._defense = defense
        self._abilities = abilities
        self._self_health_change = my_health_change
        self._opp_health_change = opponent_health_change
        self._card_draw = card_draw
        

    def update (location, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw):
        self._location = location
        self._cost = cost
        self._attack = attack
        self._defense = defense
        self._abilities = abilities
        self._self_health_change = my_health_change
        self._opp_health_change = opponent_health_change
        self._card_draw = card_draw

    def getTarget(c, burn):
        return c._defense + burn

    def getRatio(c):
        ratio = 0
        if c._card_type == 0:
            if c._cost == 0:
                ratio -= 2
            
            if c._attack >= c._cost:
                ratio += ((c._attack - c._cost) * 0.5)
            else:
                ratio += ((c._attack - c._cost))
                
            if c._defense >= c._cost:
                ratio += ((c._defense - c._cost) * 0.5)
            else:
                ratio += ((c._defense - c._cost))
                
            
            if "D" in c._abilities:
                ratio += (c._attack * 0.33333)
            if "B" in c._abilities:
                ratio += ((c._attack - 1) * 0.16666667)
        else:
            ratio += (abs(c._attack + c._defense) * 0.5)
            # TODO rajouter carte silence
            ratio -= c._cost
            
        if c._location == 0:
            ratio += (c._card_draw * 0.5)
           
        if "G" in c._abilities:
            ratio += 0.66666
        if "C" in c._abilities:
            ratio += 0.33333
        if "W" in c._abilities:
            ratio += 1
        if "L" in c._abilities:
            ratio += 0.5
        ratio += (c._self_health_change * 0.33333)
        ratio -= (c._opp_health_change * 0.33333)
        if c._cost > 10:
            ratio -= 2
        if c._cost > 8:
            ratio -= 1
        elif c._cost > 5:
            ratio -= 0.5
        
        # TODO exclusion list à enlever a terme
        if c._id in [137, 138, 139, 140, 142, 143, 148, 149, 151, 158]:
            ratio = -100
            
        if c._id in [105, 122, 103, 99, 126]:
            ratio += 0.5
        return ratio

mugu_player = Mugu_player(0, 0, 0, 0)
opp_player = Player(0, 0, 0, 0)
cards = []

mode = "Draft"

# game loop
while True:
    player_health, player_mana, player_deck, player_rune = [int(j) for j in input().split()]
    mugu_player.update(player_health, player_mana, player_deck, player_rune)

    player_health, player_mana, player_deck, player_rune = [int(j) for j in input().split()]
    opponent_hand = int(input())
    opp_player.update(player_health, player_mana, player_deck, player_rune)
    opp_player._size_hand = opponent_hand

    # draft mode
    if mugu_player._mana == 0 and opp_player._mana == 0:
        mode = "Draft"
        cards.clear()
    # battle mode
    else:
        mode = "Battle"
    
    card_count = int(input())

    for i in range(card_count):
        card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw = input().split()
        card_number = int(card_number)
        instance_id = int(instance_id)
        location = int(location)
        card_type = int(card_type)
        cost = int(cost)
        attack = int(attack)
        defense = int(defense)
        my_health_change = int(my_health_change)
        opponent_health_change = int(opponent_health_change)
        card_draw = int(card_draw)

        card = Card (card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw)

        if mode == "Battle":
            if location == 0:
                mugu_player._hand.append(card)
            elif location == 1:
                mugu_player._board.append(card)
            else:
                opp_player._board.append(card)
        else:
            cards.append ([card, i])


    if mode == "Draft":
        best_ratio = -100
        selec_card_nb = 0
        for c, nb in cards:
            ratio = Card.getRatio(c)
            print (ratio, file=sys.stderr)
            if ratio > best_ratio:
                best_ratio = ratio
                selec_card_nb = nb
        print("PICK " + str(selec_card_nb))
    else:
        battle_str = ""
        summons = ""

        # Evaluation best plays and spells, play charge
        playable_hand = list(sorted(filter(lambda c:c._cost <= mugu_player._mana, mugu_player._hand), key=Card.getRatio, reverse=True))
        for card in playable_hand:
            if card._cost <= mugu_player._mana:
                if card._card_type == 0:
                    if "C" in card._abilities:
                        battle_str += mugu_player.summon_minion(card)
                    else:
                        summons += mugu_player.summon_minion(card)
                elif card._card_type == 1 and mugu_player._board:
                    battle_str += mugu_player.use_green_item(card)
                elif card._card_type == 2 and opp_player._board:
                    battle_str += mugu_player.use_red_item(card, opp_player._board)
                elif card._card_type == 3:
                    battle_str += mugu_player.use_blue_item(card, opp_player._board)

        # fight phase
        # killing guard minions phase
        

        for minion in mugu_player._board:
            guard_minions = list(filter(lambda c:"G" in c._abilities, opp_player._board))
            if guard_minions:
                target_id = guard_minions[0]._instance_id
                opp_minion = guard_minions[0]
                    
                if not "W" in opp_minion._abilities:
                    opp_minion._defense -= minion._attack
                if "L" in minion._abilities:
                    opp_minion._defense = 0
                if not "W" in minion._abilities:
                    minion._defense -= opp_minion._attack
                if "L" in opp_minion._abilities:
                    minion._defense = 0

                if opp_minion._defense <= 0:
                    opp_player._board.remove(opp_minion)
                if minion._defense <= 0:
                    mugu_player._board.remove(minion)
            elif opp_player._board:
                if "B" in minion._abilities or "W" in minion._abilities:
                    opp_minion_list = list(filter(lambda n: not "L" in n._abilities, filter(lambda m: not "W" in m._abilities, sorted(opp_player._board, key=lambda c:c._defense))))
                    if opp_minion_list:
                        opp_minion = opp_minion_list[0]
                        target_id = opp_minion._instance_id
                        if not "W" in opp_minion._abilities:
                            opp_minion._defense -= minion._attack
                            if "L" in minion._abilities:
                                opp_minion._defense = 0
                        if not "W" in minion._abilities:
                            minion._defense -= opp_minion._attack
                            if "L" in opp_minion._abilities:
                                minion._defense = 0

                        if opp_player._board[0]._defense <= 0:
                            opp_player._board.remove(opp_minion)
                        if minion._defense <= 0:
                            mugu_player._board.remove(minion)
                    else:
                        target_id = "-1"
                else:
                    target_id = "-1"
            else:
                target_id = "-1"
            battle_str += ("ATTACK " + str(minion._instance_id) + " " + str(target_id) + ";")

        # Summonning phase
        battle_str += summons

        #
        print(battle_str)
