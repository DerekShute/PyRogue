"""
    Let's see if this all hangs together
"""
from display import Display
from game_states import QuitGame
from game_states.gameloop import MainMenuState


# Map size 80x25, but create a 80x26 display for last-line status
NUMCOLS = 80
NUMLINES = 25


def main():
    with Display(NUMCOLS, NUMLINES + 1, title='PyRogue') as d:
        try:
            loop = MainMenuState(display=d)
            while True:
                loop = loop.run()
                if loop is None:
                    break
        except QuitGame:
            raise SystemExit()


# ===== NOT TESTING =======================================

if __name__ == '__main__':
    main()

# EOF
