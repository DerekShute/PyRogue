"""
Display: tiles, windows, fonts, tilesets

Stolen liberally from tcod_tutorial_v2
"""

from typing import Any, Tuple
import tcod
from input_handler import InputHandler


class Display:
    _title: str
    # TODO: Pos()
    _xsize: int
    _ysize: int
    _console: tcod.Console

    def __init__(self, xsize: int, ysize: int, title: str = '<untitled project>'):
        self._title = title
        self._xsize = xsize
        self._ysize = ysize
        self._console = None

    def __enter__(self):
        """Handler for 'with', returns Console instance"""
        tileset = tcod.tileset.load_tilesheet("assets/terminal16x16_gs_ro.png", 16, 16, tcod.tileset.CHARMAP_CP437)
        # TODO: tileset arguments based on file used.  We could probably break out an argument list if passed a name

        self._context = tcod.context.new(columns=self._xsize, rows=self._ysize, tileset=tileset, title=self._title, vsync=True)
        self._console = tcod.Console(self._xsize, self._ysize, order="F")
        return self

    def __exit__(self, *args: Any):
        """Handler for 'with' closure"""
        # self._console only wants to be closed from the root console, so leave it alone
        self._context.close()  # via tcod/context.py __exit__
        self._context = None

    # ===== Interface Routines ============================

    @property
    def size(self):
        return self._xsize, self._ysize

    def clear(self):
        self._console.clear()

    def set_char(self, x: int, y: int, ch: int, fg: Tuple[int, int, int]):
        self._console.ch[x, y] = ch
        self._console.fg[x, y, 0] = fg[0]
        self._console.fg[x, y, 1] = fg[1]
        self._console.fg[x, y, 2] = fg[2]

    def centered_msg(self, **kwargs):
        """Print something centered horizontally"""
        pos = self._xsize // 2 - len(kwargs['string']) // 2
        self._console.print_box(x=pos, width=len(kwargs['string']), height=1, **kwargs)

    def msg(self, *args, **kwargs):
        """Print something to display, wrapper around tcod.console print"""
        self._console.print_box(height=1, width=self._xsize, *args, **kwargs)

    def present(self, player=None):
        """Perform update"""
        # Contextual to the player (the human)
        # TODO: convention is last line, but original game uses line 0
        if player is not None:
            self.msg(x=0, y=self._ysize - 1, string=player.curr_msg.ljust(self._xsize))
        self._context.present(self._console)

    def dispatch_event(self, input_handler: InputHandler) -> (InputHandler, Any):
        """Burying the TCOD details somewhere"""
        ret = None
        for event in tcod.event.wait():  # TODO: use get() for no-wait operation
            ret = input_handler.dispatch(event)
            return ret if ret is not None else (input_handler, None)

    @property
    def rgb(self):
        return self._console.tiles_rgb


# ===== Testing ===========================================

if __name__ == '__main__':
    import time

    with Display(80, 25, title='unit test Display') as d:
        d.msg(x=0, y=0, string='made it', fg=(0, 0, 255))
        d.centered_msg(y=15, string='This Should Be Centered On The Line')
        d.set_char(2, 2, ord('@'), (255, 255, 255))  # White
        d.set_char(3, 3, ord('@'), (0, 0, 255))  # Blue
        d.set_char(4, 4, ord('@'), (0, 255, 0))  # Green
        d.set_char(5, 5, ord('@'), (255, 0, 0))  # Red
        d.present()
        time.sleep(2)

    print('*** Tests Passed ***')

# EOF
