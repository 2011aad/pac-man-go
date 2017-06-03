#! /usr/bin/env python

import curses

import time

MAP_STR = """
+,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,+
|,+,-,-,-,-,-,-,-,-,-,-,-,-,+,+,-,-,-,-,-,-,-,-,-,-,-,-,+,|
|,|,.,.,.,.,.,.,.,.,.,.,.,.,|,|,.,.,.,.,.,.,.,.,.,.,.,.,|,|
|,|,.,+,-,-,+,.,+,-,-,-,+,.,|,|,.,+,-,-,-,+,.,+,-,-,+,.,|,|
|,|,I,|,,,|,.,|,,,,|,.,|,|,.,|,,,,|,.,|,,,|,I,|,|
|,|,.,+,-,-,+,.,+,-,-,-,+,.,+,+,.,+,-,-,-,+,.,+,-,-,+,.,|,|
|,|,.,,,M,,.,,,,,,.,,,.,,,,,,.,,M,,,.,|,|
|,|,.,+,-,-,+,.,+,+,,+,-,-,-,-,-,-,+,,+,+,.,+,-,-,+,.,|,|
|,|,.,+,-,-,+,.,|,|,,+,-,-,+,+,-,-,+,M,|,|,.,+,-,-,+,.,|,|
|,|,.,.,.,.,.,.,|,|,,,,,|,|,,,,,|,|,.,,,,,.,|,|
|,+,-,-,-,-,+,.,|,+,-,-,+,,|,|,,+,-,-,+,|,.,+,-,-,-,-,+,|
+,-,-,-,-,+,|,.,|,+,-,-,+,,+,+,,+,-,-,+,|,.,|,+,-,-,-,-,+
,,,,,|,|,.,|,|,.,,,,,,,,,.,|,|,.,|,|,,,,,
+,-,-,-,-,+,|,.,|,|,.,+,-,-,-,-,-,-,+,.,|,|,.,|,+,-,-,-,-,+
+,-,-,-,-,-,+,.,+,+,.,|,+,-,-,-,-,+,|,.,+,+,.,+,-,-,-,-,-,+
,,,,,,,.,,,.,|,|,,,,,|,|,.,,,.,,,,,,,
+,-,-,-,-,-,+,.,+,+,.,|,+,-,-,-,-,+,|,.,+,+,.,+,-,-,-,-,-,+
+,-,-,-,-,+,|,.,|,|,.,+,-,-,-,-,-,-,+,.,|,|,.,|,+,-,-,-,-,+
,,,,,|,|,.,|,|,.,,,,,,,,,.,|,|,.,|,|,,,,,
+,-,-,-,-,+,|,.,|,|,.,+,-,-,-,-,-,-,+,.,|,|,.,|,+,-,-,-,-,+
|,+,-,-,-,-,+,.,+,+,.,+,-,-,+,+,-,-,+,.,+,+,.,+,-,-,-,-,+,|
|,|,.,.,.,.,.,.,.,.,.,.,.,.,|,|,,,,,,,.,,,,,,|,|
|,|,.,+,-,-,+,.,+,-,-,-,+,P,|,|,,+,-,-,-,+,.,+,-,-,+,,|,|
|,|,.,+,-,+,|,.,+,-,-,-,+,,+,+,,+,-,-,-,+,.,|,+,-,+,,|,|
|,|,I,.,.,|,|,.,,,,,,,,,,,,,,,.,|,|,,,I,|,|
|,+,-,+,.,|,|,.,+,+,,+,-,-,-,-,-,-,+,M,+,+,.,|,|,,+,-,+,|
|,+,-,+,.,+,+,.,|,|,,+,-,-,+,+,-,-,+,,|,|,.,+,+,,+,-,+,|
|,|,.,,.,,,.,|,|,,,,,|,|,,,,,|,|,.,,,,,,|,|
|,|,.,+,-,-,-,-,+,+,-,-,+,,|,|,,+,-,-,+,+,-,-,-,-,+,,|,|
|,|,.,+,-,-,-,-,-,-,-,-,+,,+,+,,+,-,-,-,-,-,-,-,-,+,,|,|
|,|,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,|,|
|,+,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,+,|
+,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,+
"""
CAPSULE = 'I'
PACMAN = 'P'
GHOST = 'M'
FOOD = '.'

MAP = []
INIT_PACMAN = None
INIT_GHOST = None


def init_screen(screen):
    curses.curs_set(0)
    curses.halfdelay(200)

    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    style = {
        "|": curses.color_pair(1) | curses.A_REVERSE,
        "+": curses.color_pair(1) | curses.A_REVERSE,
        "-": curses.color_pair(1) | curses.A_REVERSE,
        ".": curses.color_pair(2),
        "P": curses.color_pair(2) | curses.A_BOLD | curses.A_REVERSE,
        "M": curses.color_pair(3) | curses.A_BOLD | curses.A_REVERSE,
        "I": curses.color_pair(0) | curses.A_BOLD | curses.A_REVERSE | curses.A_BLINK,
    }

    screen.clear()

    game_state = GameState()

    row = 0
    for line in MAP_STR.strip().split("\n"):
        row = row + 1
        col = 0
        MAP.append([])
        for ch in line.strip().split(","):
            col = col + 1
            if ch:
                # screen.addstr(row, col, ch, style[ch])
                MAP[-1].append(ch)
                if ch == PACMAN:
                    pac = Pacman()
                    pac.pos = (row-1, col-1)
                    INIT_PACMAN = pac.pos
                    game_state.agent_states.append(pac)
                if ch == FOOD:
                    game_state.foods.append((row-1, col-1))
                if ch == GHOST:
                    ghost = Ghost()
                    ghost.pos = (row-1, col-1)
                    INIT_GHOST = ghost.pos
                    game_state.agent_states.append(ghost)
                if ch == CAPSULE:
                    game_state.capsules.append((row-1, col-1))
            else:
                MAP[-1].append(' ')
                # TODO update game_state
    for i in range(len(game_state.agent_states)):
        if isinstance(game_state.agent_states[i], Pacman):
            game_state.agent_states[i], game_state.agent_states[0] = game_state.agent_states[0], game_state.agent_states[i]

    display(screen, style, game_state)

    while True:
        time.sleep(5)
        (row, col) = game_state.agent_states[0].pos
        game_state.agent_states[0].pos = (row + 1, col)
        display(screen, style, game_state)
        pass

    #run(screen, style, game_state)


TIME_STEP = 100
STEP_DURATION = 0.5

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
STOP = (0, 0)


class GameState:
    def __init__(self):
        self.agent_states = []
        self.foods = []
        self.capsules = []
        self.score = 0

    def generate_successor(self, index, action):
        """ return a new game_state """
        pass

    def get_legal_actions(self, index):
        """ return a list of action """


class AgentState:
    def __init__(self):
        self.pos = (0, 0)
        self.dir = STOP
        self.speed = 1
        self.capsule_timer = 0
        pass

    def get_action(self, game_state):
        """ return an action """
        pass


class Pacman(AgentState):
    def __init__(self):
        AgentState.__init__(self)
        self.num_ghost_eaton = 0
        self.num_died = 0


class Ghost(AgentState):
    def __init__(self):
        AgentState.__init__(self)


def run(screen, style, game_state):
    for crt_time in range(TIME_STEP):
        begin = time.clock()
        for index in range(len(game_state.agent_states)):
            agent_state = game_state.agent_states[index]
            if crt_time % agent_state.speed == 0:
                action = agent_state.get_action(game_state)
                game_state = game_state.generate_successor(index, action)
                display(screen, style, game_state)
        spend = min(STEP_DURATION, time.clock() - begin)
        sleep_time = STEP_DURATION - spend
        time.sleep(sleep_time)


def display(screen, style, game_state):
    screen.clear()
    for row in range(len(MAP)):
        for col in range(len(MAP[row])):
            ch = MAP[row][col]
            if ch == '+' or ch == '-' or ch == '|':
                screen.addstr(row, col, ch, style[ch])

    for food in game_state.foods:
        screen.addstr(food[0], food[1], FOOD, style[FOOD])

    for cap in game_state.capsules:
        screen.addstr(cap[0], cap[1], CAPSULE, style[CAPSULE])

    for agent in game_state.agent_states:
        if isinstance(agent, Pacman):
            screen.addstr(agent.pos[0], agent.pos[1], PACMAN, style[PACMAN])
        else:
            screen.addstr(agent.pos[0], agent.pos[1], GHOST, style[GHOST])
    screen.refresh()


def debug(info):
    pass


def main():
    curses.wrapper(init_screen)

if __name__ == "__main__":
    main()
