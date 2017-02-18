import pygame

from drawing_surface import easel
from game_objects import TableFactory
from player import Player
from settings import config
from buttons import buttons
from holding_area import holding_area

class Game(object):
    def __init__(self):
        self.table = None
        self.players = None

    @property
    def player_count(self):
        return len(self.players)

    @property
    def current_player(self):
        return [p for p in self.players if p.state == 'turn started'][0]

    def embody(self):
        self.table.embody()
        for player in self.players:
            player.embody()

        # TODO: Better place for this?
        holding_area.embody(config.holding_area_location)


class GameFactory(object):
    def __init__(self):
        pass

    def __call__(self, player_names):
        game = Game()

        game.players = [Player(name, i)
                        for (i, name) in enumerate(player_names)]
        table_factory = TableFactory()
        game.table = table_factory(game.player_count)

        # TODO Refactor this?
        game.players[0].start()

        return game


def refresh_display():
    theApp.the_game.embody()
    pygame.display.flip()


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.game_state = None
        self.the_game = None
        self.size = \
            self.weight, self.height = \
            config.tabletop_size.x * config.scaling_factor, \
            config.tabletop_size.y * config.scaling_factor

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self._running = True
        easel.init_easel(self._display_surf)
        game_factory = GameFactory()
        self.the_game = game_factory(
            player_names=['Caroline', 'Nigel', 'Issie', 'Coen']
        )
        refresh_display()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if buttons.process_mouse_click(self.the_game.current_player):
                refresh_display()

    def on_loop(self):
        pass

    def on_render(self):
        pass

    @staticmethod
    def on_cleanup():
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
