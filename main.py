#! /usr/bin/env python
import copy
import curses
from pprint import pprint

import time
import random

MAP_STR = """
+,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,+
|,+,-,-,-,-,-,-,-,-,-,-,-,-,+,+,-,-,-,-,-,-,-,-,-,-,-,-,+,|
|,|,.,.,.,.,.,.,.,.,.,.,.,.,|,|,.,.,.,.,.,.,.,.,.,.,.,.,|,|
|,|,.,+,-,-,+,.,+,-,-,-,+,.,|,|,.,+,-,-,-,+,.,+,-,-,+,.,|,|
|,|,I,|,,,|,.,|,,,,|,.,|,|,.,|,,,,|,.,|,,,|,I,|,|
|,|,.,+,-,-,+,.,+,-,-,-,+,.,+,+,.,+,-,-,-,+,.,+,-,-,+,.,|,|
|,|,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,|,|
|,|,.,+,-,-,+,.,+,+,.,+,-,-,-,-,-,-,+,.,+,+,.,+,-,-,+,.,|,|
|,|,.,+,-,-,+,.,|,|,.,+,-,-,+,+,-,-,+,.,|,|,.,+,-,-,+,.,|,|
|,|,.,.,.,.,.,.,|,|,.,.,.,.,|,|,.,.,.,.,|,|,.,.,.,.,.,.,|,|
|,+,-,-,-,-,+,.,|,+,-,-,+,.,|,|,.,+,-,-,+,|,.,+,-,-,-,-,+,|
+,-,-,-,-,+,|,.,|,+,-,-,+,.,+,+,.,+,-,-,+,|,.,|,+,-,-,-,-,+
,,,,,|,|,.,|,|,.,.,.,.,.,.,.,.,.,.,|,|,.,|,|,,,,,
+,-,-,-,-,+,|,.,|,|,.,+,-,-,,,-,-,+,.,|,|,.,|,+,-,-,-,-,+
+,-,-,-,-,-,+,.,+,+,.,|,+,-,,,-,+,|,.,+,+,.,+,-,-,-,-,-,+
.,.,.,.,.,.,.,.,.,.,.,|,|,M,M,M,M,|,|,.,.,.,.,.,.,.,.,.,.,.
+,-,-,-,-,-,+,.,+,+,.,|,+,-,-,-,-,+,|,.,+,+,.,+,-,-,-,-,-,+
+,-,-,-,-,+,|,.,|,|,.,+,-,-,-,-,-,-,+,.,|,|,.,|,+,-,-,-,-,+
,,,,,|,|,.,|,|,.,.,.,P,.,.,.,.,.,.,|,|,.,|,|,,,,,
+,-,-,-,-,+,|,.,|,|,.,+,-,-,-,-,-,-,+,.,|,|,.,|,+,-,-,-,-,+
|,+,-,-,-,-,+,.,+,+,.,+,-,-,+,+,-,-,+,.,+,+,.,+,-,-,-,-,+,|
|,|,.,.,.,.,.,.,.,.,.,.,.,.,|,|,.,.,.,.,.,.,.,.,.,.,.,.,|,|
|,|,.,+,-,-,+,.,+,-,-,-,+,.,|,|,.,+,-,-,-,+,.,+,-,-,+,.,|,|
|,|,.,+,-,+,|,.,+,-,-,-,+,.,+,+,.,+,-,-,-,+,.,|,+,-,+,.,|,|
|,|,I,.,.,|,|,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,|,|,.,.,I,|,|
|,+,-,+,.,|,|,.,+,+,.,+,-,-,-,-,-,-,+,.,+,+,.,|,|,.,+,-,+,|
|,+,-,+,.,+,+,.,|,|,.,+,-,-,+,+,-,-,+,.,|,|,.,+,+,.,+,-,+,|
|,|,.,.,.,.,.,.,|,|,.,.,.,.,|,|,.,.,.,.,|,|,.,.,.,.,.,.,|,|
|,|,.,+,-,-,-,-,+,+,-,-,+,.,|,|,.,+,-,-,+,+,-,-,-,-,+,.,|,|
|,|,.,+,-,-,-,-,-,-,-,-,+,.,+,+,.,+,-,-,-,-,-,-,-,-,+,.,|,|
|,|,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,|,|
|,+,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,+,|
+,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,+
"""
CAPSULE = 'I'
PACMAN = 'P'
GHOST = 'M'
FOOD = '.'
WALL = {'+', '-', '|'}

MAP = []
INIT_PACMAN = None
INIT_GHOST = None
DIS = {}
xxxx = {}

def init_screen(screen):
    curses.curs_set(0)
    curses.halfdelay(100)

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
                    global INIT_PACMAN
                    INIT_PACMAN = pac.pos
                    game_state.agent_states.append(pac)
                if ch == FOOD:
                    game_state.foods.append((row-1, col-1))
                if ch == GHOST:
                    ghost = Ghost()
                    ghost.pos = (row-1, col-1)
                    global INIT_GHOST
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
    for i in range(len(game_state.agent_states)):
        game_state.agent_states[i].index = i

    ps = [(i, j) for i in range(len(MAP)) for j in range(len(MAP[0]))]
    for i in range(len(ps)):
        for j in range(len(ps)):
            DIS[(ps[i], ps[j])] = 100000
            if i == j:
                DIS[(ps[i], ps[j])] = 0
            a = ps[i]
            b = ps[j]
            if MAP[a[0]][a[1]] not in WALL and MAP[b[0]][b[1]] not in WALL and abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1:
                DIS[(a, b)] = 1
    for k in range(len(ps)):
        for i in range(len(ps)):
            if DIS[(ps[i], ps[k])] > 9999:
                continue
            for j in range(len(ps)):
                if DIS[(ps[i], ps[j])] < DIS[(ps[i], ps[k])] + DIS[(ps[k], ps[j])]:
                    DIS[(ps[i], ps[j])] = DIS[(ps[i], ps[k])] + DIS[(ps[k], ps[j])]
    display(screen, style, game_state)

    # while True:
    #     time.sleep(5)
    #     (row, col) = game_state.agent_states[0].pos
    #     game_state.agent_states[0].pos = (row + 1, col)
    #     display(screen, style, game_state)
    #     pass

    run(screen, style, game_state)


TIME_STEP = 100
STEP_DURATION = 1
CAPSULE_TIMEOUT = 10

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
STOP = (0, 0)
ACTIONS = [STOP, UP, DOWN, LEFT, RIGHT]


class GameState:
    def __init__(self):
        self.agent_states = []
        self.foods = []
        self.capsules = []
        self.score = 0

    def generate_successor(self, index, action):
        """ return a new game_state """
        if action not in self.get_legal_actions(index):
            action = STOP

        game_state = self._clone()
        agents = game_state.agent_states
        ai = agents[index]
        ai.dir = action
        ai.pos = ai.pos[0] + action[0], ai.pos[1] + action[1]

        # check and update
        if isinstance(ai, Pacman):
            if ai.pos in game_state.foods:
                game_state.score += 10
                game_state.foods.remove(ai.pos)
            if ai.pos in game_state.capsules:
                game_state.capsules.remove(ai.pos)
                for agent in agents:
                    agent.capsule_timer = CAPSULE_TIMEOUT
        for oi in range(len(agents)):
            if oi != index:
                ao = agents[oi]
                if ao.pos == ai.pos:
                    # meet
                    pac, gho = None, None
                    if isinstance(ai, Pacman) and isinstance(ao, Ghost):
                        pac, gho = ai, ao
                    elif isinstance(ai, Ghost) and isinstance(ao, Pacman):
                        pac, gho = ao, ai
                    if pac is not None and gho is not None:
                        if gho.capsule_timer > 0:
                            # ghost died
                            gho.pos = INIT_GHOST
                            gho.dir = STOP
                            gho.capsule_timer = 0
                            gho.speed = 1

                            pac.num_ghost_eaton += 1
                            game_state.score += 200 * pac.num_ghost_eaton
                        else:
                            # pacman died
                            pac.pos = INIT_PACMAN
                            pac.dir = STOP

                            pac.num_died += 1
                            if pac.num_died == 3:
                                raise Exception('Pacman died 3 times, Points: ' + str(game_state.score))
            if agents[oi].capsule_timer > 0:
                agents[oi].capsule_timer -= 1
                if agents[oi].capsule_timer == 0 and isinstance(agents[oi], Pacman):
                    agents[oi].num_ghost_eaton = 0
        return game_state

    def _clone(self):
        game_state = GameState()
        game_state.foods = self.foods[:]
        game_state.capsules = self.capsules[:]
        game_state.score = self.score
        game_state.agent_states = [copy.copy(a) for a in self.agent_states]
        return game_state

    def get_legal_actions(self, index):
        """ return a list of action """
        actions = []
        agent = self.agent_states[index]
        for action in ACTIONS:
            pos = agent.pos[0] + action[0], agent.pos[1] + action[1]
            if MAP[pos[0]][pos[1]] not in WALL:
                actions.append(action)
        return actions


class AgentState:
    def __init__(self):
        self.index = -1
        self.pos = (0, 0)
        self.dir = STOP
        self.speed = 1
        self.capsule_timer = 0
        pass

    def get_action(self, game_state, screen):
        """ return an action """
        legal = game_state.get_legal_actions(self.index)
        return random.choice(legal)


class Pacman(AgentState):
    def __init__(self):
        AgentState.__init__(self)
        self.num_ghost_eaton = 0
        self.num_died = 0

    def get_action(self, game_state, screen):
        event = screen.getch()
        if event == ord('w'):
            return UP
        if event == ord('s'):
            return DOWN
        if event == ord('a'):
            return LEFT
        if event == ord('d'):
            return RIGHT
        return self.dir

AI_DEPTH = 1

class Ghost(AgentState):
    def __init__(self):
        AgentState.__init__(self)

    def get_action(self, game_state, screen):
        return min([(DIS[(game_state.generate_successor(self.index, action).agent_states[self.index].pos,
                          game_state.agent_states[0].pos)], action)
                    for action in game_state.get_legal_actions(self.index)])[1]
        # return random.choice(game_state.get_legal_actions(self.index))
        return self.minimax(game_state, 0)[1]

    def minimax(self, game_state, layer):
        if layer == AI_DEPTH * len(game_state.agent_states):
            return self.evaluate(game_state), None
        id = (self.index + layer) % len(game_state.agent_states)
        score_actions = []
        for action in game_state.get_legal_actions(id):
            score_actions.append((self.minimax(game_state, layer + 1), action))
        if layer % len(game_state.agent_states) == 0:
            score = max(score_actions)
        else:
            score = min(score_actions)
        ch = [a for s, a in score_actions if s == score[0]]
        return score, random.choice(ch)

    def evaluate(self, game_state):
        agents = game_state.agent_states
        score = -game_state.score
        me = agents[self.index]
        if me.capsule_timer > 0:
            score -= DIS[(me.pos, agents[0].pos)] * 0.1
        else:
            score += DIS[(me.pos, agents[0].pos)] * 0.1
        return -DIS[(me.pos, agents[0].pos)]
        return score


def run(screen, style, game_state):
    for crt_time in range(TIME_STEP):
        begin = time.clock()
        for index in range(len(game_state.agent_states)):
            agent_state = game_state.agent_states[index]
            if crt_time % agent_state.speed == 0:
                action = agent_state.get_action(game_state, screen)
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
    #game_state.
    screen.refresh()

def debug(info):
    pass


def main():
    curses.wrapper(init_screen)

if __name__ == "__main__":
    main()
