import pygame

from drawing_surface import easel
from logical_game_objects import Table
from settings import config

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.game_state = None
        self.size = \
            self.weight, self.height = \
            config.tabletop_width * config.scaling_factor, \
            config.tabletop_height * config.scaling_factor

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self._running = True
        easel.init_easel(self._display_surf)
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
