"""
Display: tiles, windows, fonts, tilesets

Stolen liberally from tcod_tutorial_v2
"""

import tcod
from typing import Any

class Display:
    _title: str
    # TODO: Pos()
    _xsize: int
    _ysize: int

    def __init__(self, xsize:int, ysize:int, title:str='<untitled project>'):
        self._title = title
        self._xsize = xsize
        self._ysize = ysize
        self._console:Console = None

    def __enter__(self):
        """Handler for 'with', returns Console instance"""
        tileset = tcod.tileset.load_tilesheet("assets/terminal16x16_gs_ro.png", 16, 16, tcod.tileset.CHARMAP_CP437)
        # TODO: tileset arguments based on file used.  We could probably break out an argument list if passed a name
        
        self._context = tcod.context.new(columns=self._xsize, rows=self._ysize, tileset=tileset, title=self._title, vsync=True)
        self._console = tcod.Console(self._xsize, self._ysize, order="F")
        return self

    def __exit__(self, *args: Any):
        """Handler for 'with' closure"""
        self._console.close()  # via tcod/console.py __exit__
        self._console = None
        self._context.close()  # via tcod/context.py __exit__
        self._context = None

    # ===== Interface Routines ============================

    def print(self, *args, **kwargs):
        """Print something to display, wrapper around tcod.console print"""
        self._console.print(*args, **kwargs)

    def present(self):
        """Perform update"""
        self._context.present(self._console)

# ===== Testing ===========================================

if __name__=='__main__':
    import time
    
    with Display(80, 25, title='unit test Display') as d:
        d.print(0, 0, 'made it')
        d.present()
        time.sleep(10)
    
    print('*** Tests Passed ***')