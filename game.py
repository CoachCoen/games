import pygame

from drawing_surface import easel
from game_objects import TableFactory, holding_area
from player import Player
from settings import config
from buttons import buttons
# from holding_area import holding_area
from game_state import game_state

class Game(object):
    def __init__(self):
        self.table = None
        self.players = None
        self.holding_area = None

    @property
    def player_count(self):
        return len(self.players)

    @property
    def current_player(self):
        return [p for p in self.players if p.state != 'waiting for turn'][0]

    def next_player(self):
        current = self.current_player
        current.confirm()
        i = self.players.index(current)
        try:
            next_p = self.players[i + 1]
        except IndexError:
            next_p = self.players[0]

        next_p.start()

    def embody(self):
        v_a = game_state.valid_actions
        buttons.reset()
        self.table.embody()
        for player in self.players:
            player.embody()
        self.holding_area.embody(config.holding_area_location)


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

        game.holding_area = holding_area

        return game


def refresh_display():
    game_state.update(theApp.the_game)
    theApp.the_game.embody()
    pygame.display.flip()


def next_player():
    theApp.the_game.next_player()


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
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
            # player_names=['Caroline', 'Nigel', 'Issie', 'Coen']
            player_names = ['Caroline', 'Nigel']
        )
        refresh_display()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.MOUSEBUTTONUP:
            events = buttons.process_mouse_click(self.the_game.current_player)

            # TODO: Better way to pass this back
            for event in events:
                {
                    'refresh_display': refresh_display,
                    'next_player': next_player
                }[event]()

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
