import pygame

# from drawing import Table, SCALING_FACTOR
# from drawing import easel
# from game_state import GameState

from drawing_surface import SCALING_FACTOR, easel
from logical_game_objects import Table

TABLETOP_WIDTH = 1366
TABLETOP_HEIGHT = 768

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.game_state = None
        self.size = \
            self.weight, self.height = \
            TABLETOP_WIDTH * SCALING_FACTOR, \
            TABLETOP_HEIGHT * SCALING_FACTOR

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self._running = True
        easel.init_easel(self._display_surf, TABLETOP_WIDTH, TABLETOP_HEIGHT)
        # self.game_state = GameState(players=['Coen', 'Sue', 'John'])
        table = Table(players=['Coen', 'Sue', 'John'])
        table.draw()

        pygame.display.flip()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() is False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
