"""
Main module - game initialisation and flow
"""

import pygame

from drawing_surface import easel
from game_objects import Table, HoldingArea
from player import Player
from settings import config
from buttons import buttons
# from game_state import GameState
from ai_simple import RandomAI
from game_game import game


def init_game(player_details):
    """
    Create players, table and holding area
    :param player_details: list of (player name, player's AI)
    """
    players = [
        Player(
            name=name,
            AI=AI,
            player_order=i
        )
        for (i, (name, AI)) in enumerate(player_details)]

    # table = TableFactory()(len(players))

    game.init_game(
        players=players,
        table=Table(len(players)),
        holding_area=HoldingArea(),
        # game_state=GameState(),
        buttons=buttons
    )


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None

    def on_init(self):
        """
        Initialisation, called before the main game loop
        """
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            list(config.tabletop_size * config.scaling_factor),
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        easel.init_easel(self._display_surf)
        init_game(
            player_details=[
                ('Caroline', RandomAI()),
                ('Nigel', RandomAI()),
                ('Issie', RandomAI()),
                ('Coen', None)
            ]
        )

        # player[0] is the start player
        game.players[0].start()

        game.refresh_display()

        # Notify main game loop that the initialisation is done
        self._running = True

    def on_event(self, event):
        """
        Process a pygame event
        :param event: the event
        """
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.MOUSEBUTTONUP:
            game.buttons.process_mouse_click(game.current_player)

    @staticmethod
    def on_cleanup():
        """
        Called after main game loop,
        any clean up actions
        """
        pygame.quit()

    def on_execute(self):
        """
        Main code - initialise, main game loop, clean up
        """
        if self.on_init() is False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)

        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
