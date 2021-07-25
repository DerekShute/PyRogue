"""
    Used to target a location.  Stolen liberally from tcod tutorial
"""
import tcod
from game_states import InputHandler, CancelHandler
from actions import Action
from position import Pos

# ===== TargetInputHandler ================================

class TargetInputHandler(InputHandler):
    """Select a location on the map/screen"""
    msg: str
    action: Action

    def __init__(self, action: Action = None, msg: str = '', usage: str = '', **kwargs):
        super().__init__(**kwargs)
        self.inventory = None
        self.msg = msg
        self.action = action

    def render_layer(self, display):
        xsize, ysize = display.size
        display.msg(x=0, y=ysize - 1, string=self.msg.ljust(xsize))

    def ev_quit(self, event: tcod.event.Quit):
        return CancelAction()

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown):
        """Left click confirms a selection."""
        if event.button == 1:
            return self.action.incorporate(pos=Pos(event.tile.x, event.tile.y))
        return super().ev_mousebuttondown(event)

    def ev_keydown(self, event: tcod.event.KeyDown):
        if event.sym == tcod.event.K_ESCAPE:  # "Abort the mission"
            return self.previous
        return super().ev_keydown(event)

# EOF
