import tcod
from game_states import InputHandler, CancelHandler
from actions import ChatAction


# ===== ChatInputHandler ================================

class ChatInputHandler(InputHandler):
    """Base input handler for ordinary game input"""
    text: str = ''

    def ev_quit(self, event: tcod.event.Quit):
        return CancelHandler()  # Out the door immediately

    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.sym

        if key == tcod.event.K_ESCAPE:  # Never mind.
            return self.previous

        if key == tcod.event.K_RETURN:  # End of chat message.
            return ChatAction(self.text)

        if key >= tcod.event.K_SPACE and key <= tcod.event.K_z:
            # TODO: add to string.  Is string actually a list?
            # TODO: if shift, capitalize
            self.text = self.text + chr(key)
            return self

        if key == tcod.event.K_BACKSPACE:
            # TODO: remove last string element
            self.text = self.text.rstrip(self.text[-1])
            return self

        return self

    def render_layer(self, display):
        xsize, ysize = display.size
        text = f'chat: {self.text}'
        display.msg(x=0, y=ysize - 1, string=text.ljust(xsize))

# EOF
