#! /usr/bin/env python

import curses

import time

MAP = """
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
    for line in MAP.strip().split("\n"):
        row = row + 1
        col = 0
        for ch in line.strip().split(","):
            col = col + 1
            if ch:
                screen.addstr(row, col, ch, style[ch])

    run(screen, game_state)
    screen.refresh()
    screen.addstr(7, 8, 'I', style['I'])
    time.sleep(10)
    while True:
        screen.refresh()
        # event = screen.getch()
        # if event == 27:
        #     pass
            # break

TIME_STEP = 100
STEP_DURATION = 0.5


class GameState:
    pass

def run(screen, game_state):
    for crt_time in range(TIME_STEP):
        begin = time.clock()
        for agent_state in game_state.agent_states:
            if crt_time % agent_state.speed == 0:
                action = agent_state.getAction(game_state)
                game_state = agent_state.generateSuccessor(game_state, action)
                display(screen, game_state)
        spend = min(STEP_DURATION, time.clock() - begin)
        sleep_time = STEP_DURATION - spend
        time.sleep(sleep_time)


def debug(info):
    pass

def main():
    curses.wrapper(init_screen)

if __name__ == "__main__":
    main()
