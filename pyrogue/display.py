"""
Display: tiles, windows, fonts, tilesets

Stolen liberally from tcod_tutorial_v2
"""

from typing import Any, Tuple
import tcod
from game_states import InputHandler
from menu import Menu


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

    def present(self):
        """Perform update"""
        self._context.present(self._console)

    def dispatch_event(self, input_handler: InputHandler) -> Tuple[InputHandler, Any]:
        """Burying the TCOD details somewhere"""
        ret = None
        for event in tcod.event.wait():  # TODO: use get() for no-wait operation
            self._context.convert_event(event)  # mouse pixel -> tile
            ret = input_handler.dispatch(event)
            return ret if ret is not None else (input_handler, None)

    def display(self, input_handler: InputHandler, player) -> Tuple[InputHandler, Any]:
        """Burying the TCOD details somewhere"""
        input_handler.render_layer(self)
        self.present()
        if player.msg_count > 1:
            for event in tcod.event.wait():
                if event.type == 'KEYDOWN':
                    player.advance_msg()
            return (input_handler, None)
        return self.dispatch_event(input_handler)

    def draw_menu(self, x: int, menu: Menu):
        x = 42 if x <= 40 else 0
        y = 1
        width = 30
        height = len(menu.text) + 2
        self._console.draw_frame(x=x, y=0, width=width, height=height, title=menu.title, clear=True,
                                 fg=(255, 255, 255), bg=(50, 50, 50))
        for line in menu.text:
            self._console.print(x=x + 1, y=y, string=line)
            y = y + 1

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
