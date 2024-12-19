import random
import math

def print_welcome():
    print("\t\tMINOTAUR")
    print("\tCREATIVE COMPUTING, MORRISTOWN, NEW JERSEY")
    print("\nDO YOU WANT TO BE THE MINOTAUR CHAMPION? YOU MUST BEAT A SCORE OF 20.")

def print_instructions():
    print("\n******************** MINOTAUR ********************")
    print("THE OBJECT OF THE GAME IS TO KILL THE MINOTAUR")
    print("\n******************** CAVERN ********************")
    print("THE CAVERN OF THE MINOTAUR IS IN THREE LEVELS.")
    print("EACH LEVEL IS A COORDINATE PLANE. OUTSIDE OF THE LEVELS, THERE IS NOTHING BUT VACUUM.")
    print("THE PLANES STRETCH OUT 10 ON EACH AXIS FROM THE ORIGIN.")
    print("\n******************** HAZARDS ********************")
    print("BARRIERS: INSIDE THE CAVERN ARE 10 ELECTRIFIED PILLARS.")
    print("THEY WILL DESTROY ANYTHING THAT TOUCHES THEM!!")
    print("\nTRAPDOORS: TRAPDOORS WILL APPEAR OUT OF NOWHERE AND DROP YOU DOWN ONE LEVEL.")
    print("IF YOU WERE ON LEVEL ONE, YOU LOSE!!")
    print("\n******************** CONTROLS ********************")
    print("1) MOVE EAST\n2) MOVE WEST\n3) MOVE NORTH\n4) MOVE SOUTH\n5) MOVE UP A LEVEL\n6) MOVE DOWN A LEVEL\n7) THROW SPEAR\n8) GET A MAP")
    print("\nHAVE FUN!")

def initialize_game():
    player = {
        'level': random.randint(1, 3),
        'x': random.randint(-10, 10),
        'y': random.randint(-10, 10),
        'spear': True
    }

    minotaur = {
        'level': random.randint(1, 3),
        'x': random.randint(-10, 10),
        'y': random.randint(-10, 10)
    }

    barriers = [(random.randint(-10, 10), random.randint(-10, 10)) for _ in range(10)]

    return player, minotaur, barriers

def print_status(player, minotaur, turn):
    print(f"\nTURN {turn}")
    print(f"YOU ARE AT ({player['x']}, {player['y']}) ON LEVEL {player['level']}.")
    print(f"MINOTAUR IS AT ({minotaur['x']}, {minotaur['y']}) ON LEVEL {minotaur['level']}.")

def move_player(player, direction):
    if direction == 1:  # East
        player['x'] += 1
    elif direction == 2:  # West
        player['x'] -= 1
    elif direction == 3:  # North
        player['y'] += 1
    elif direction == 4:  # South
        player['y'] -= 1
    elif direction == 5:  # Up
        player['level'] += 1
    elif direction == 6:  # Down
        player['level'] -= 1

def check_boundaries(player):
    if abs(player['x']) > 10 or abs(player['y']) > 10 or player['level'] < 1 or player['level'] > 3:
        print("YAAAAAAAAAAAAAAAAH YOU FELL OFF THE EDGE")
        return True
    return False

def check_barriers(player, barriers):
    if (player['x'], player['y']) in barriers:
        print("YOU FRIED YOURSELF ON AN ELECTRIFIED BARRIER!")
        return True
    return False

def trapdoor(player):
    if random.random() < 0.1:
        print("YAAAAAAAAAAAAAAH TRAPDOOR, YOU FELL DOWN ONE LEVEL")
        player['level'] -= 1
        if player['level'] < 1:
            print("YOU FELL OUT OF THE CAVERN. YOU LOSE.")
            return True
    return False

def throw_spear(player, minotaur):
    if player['level'] != minotaur['level']:
        print("YOU ARE NOT ON THE SAME LEVEL AS THE MINOTAUR. YOU CANNOT THROW.")
        return False

    dx = abs(player['x'] - minotaur['x'])
    dy = abs(player['y'] - minotaur['y'])

    if dx > 10 or dy > 10:
        print("THE MINOTAUR IS TOO FAR AWAY TO HIT.")
        return False

    if player['x'] == minotaur['x'] or player['y'] == minotaur['y']:
        print("YOU KILLED THE MINOTAUR!")
        return True

    print("YOU MISSED. THE MINOTAUR IS STILL ALIVE.")
    player['spear'] = False
    return False

def minotaur_charge(minotaur, player):
    if random.random() < 0.3:
        print("THE MINOTAUR IS CHARGING!")
        minotaur['x'] += math.copysign(1, player['x'] - minotaur['x'])
        minotaur['y'] += math.copysign(1, player['y'] - minotaur['y'])
        if minotaur['x'] == player['x'] and minotaur['y'] == player['y'] and minotaur['level'] == player['level']:
            print("THE MINOTAUR CAUGHT YOU. YOU LOSE!")
            return True
    return False

def print_map(player, minotaur, barriers, level):
    print(f"\nMAP OF LEVEL {level}")
    for y in range(10, -11, -1):
        for x in range(-10, 11):
            if (x, y) == (player['x'], player['y']) and level == player['level']:
                print('Y', end=' ')
            elif (x, y) == (minotaur['x'], minotaur['y']) and level == minotaur['level']:
                print('M', end=' ')
            elif (x, y) in barriers:
                print('B', end=' ')
            elif x == 0 and y == 0:
                print('O', end=' ')
            elif x == 0 or y == 0:
                print('X', end=' ')
            else:
                print('.', end=' ')
        print()
    
    print("\nKEY:")
    print("Y = YOU")
    print("M = MINOTAUR")
    print("B = BARRIER")
    print("O = ORIGIN")
    print("X = AXIS")

def get_valid_move():
    while True:
        try:
            move = int(input("YOUR MOVE (1-8): "))
            if 1 <= move <= 8:
                return move
            print("PLEASE ENTER A NUMBER BETWEEN 1 AND 8")
        except ValueError:
            print("PLEASE ENTER A VALID NUMBER")

def calculate_score(turns):
    return int((1/turns) * 100)

def main():
    print_welcome()
    if input("DO YOU NEED INSTRUCTIONS? (YES/NO): ").strip().upper() == "YES":
        print_instructions()

    player, minotaur, barriers = initialize_game()
    turn = 0

    while True:
        turn += 1
        print_status(player, minotaur, turn)

        if trapdoor(player):
            break

        move = get_valid_move()
        if move in range(1, 7):
            move_player(player, move)
            if check_boundaries(player) or check_barriers(player, barriers):
                break

        elif move == 7:
            if player['spear']:
                if throw_spear(player, minotaur):
                    print(f"YOU WON IN {turn} TURNS! YOU ARE THE CHAMPION!")
                    break
            else:
                print("YOU HAVE NO SPEAR TO THROW.")

        elif move == 8:
            print_map(player, minotaur, barriers, player['level'])

        if minotaur_charge(minotaur, player):
            break
if __name__ == "__main__":
    main()
