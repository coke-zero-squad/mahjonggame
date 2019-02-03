import random
import fileinput

suits = {
    0: "dots",
    1: "bamboo",
    2: "characters",
    3: "winds",
    4: "dragons",
}

values = {
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "east",
    11: "south",
    12: "west",
    13: "north",
    14: "white",
    15: "green",
    16: "red",
}

class Suit:
    DOT = 0
    BAMBOO = 1
    CHARACTER = 2
    WIND = 3
    DRAGON = 4

class Wind:
    EAST = 10
    SOUTH = 11
    WEST = 12
    NORTH = 13

class Dragon:
    WHITE = 14
    GREEN = 15
    RED = 16

class Tile:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def is_honor(self):
        return self.value > 9

    def __repr__(self):
        return values[self.value] + " of " + suits[self.suit]

    def __str__(self):
        return values[self.value] + " of " + suits[self.suit]

class Player:
    def __init__(self, seat):
        self.seat = seat
        self.hand = []
        self.discards = []

    def __str__(self):
        r = ""
        for tile in self.hand:
            r += str(tile) + "\n"
        return r

    def draw(self, state, count = 1):
        for i in range(count):
            self.hand.append(state.wall.pop())

    def discard(self, tile_index):
        self.discards.append(self.hand.pop(tile_index))

class GameState:
    current_player_index = 0

    def __init__(self, players, wall):
        self.players = players
        self.wall = wall

    def increment_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def current_player(self):
        return self.players[self.current_player_index]

def generate_wall():
    tiles = []
    for suit in range(Suit.CHARACTER + 1):
        for value in range(1, 10):
            tiles.append(Tile(suit, value))
    for value in range(Wind.EAST, Wind.NORTH + 1):
        tiles.append(Tile(Suit.WIND, value))
    for value in range(Dragon.WHITE, Dragon.RED + 1):
        tiles.append(Tile(Suit.DRAGON, value))
    return tiles + tiles + tiles + tiles

def initial_draw(state):
    for i in range(3 * len(state.players)):
        player = state.current_player()
        player.draw(state, 4)
        state.increment_player()

    for i in range(len(state.players)):
        player = state.current_player()
        player.draw(state)
        state.increment_player()

def init_game():
    wall = generate_wall()
    random.shuffle(wall)
    players = list(map(lambda wind: Player(wind), range(Wind.EAST, Wind.NORTH + 1)))
    state = GameState(players, wall)

    initial_draw(state)

    return state

def discard(state, args):
    index = int(args[0])
    state.current_player().discard(index)
    state.increment_player()
    return state

def handle_command(state, command, args):
    return {
        "discard": discard,
    }[command](state, args)

def main():
    state = init_game()

    for input in fileinput.input():
        command, *args = input.split()

        state = handle_command(state, command.strip(), args)
    fileinput.close()

    return state
