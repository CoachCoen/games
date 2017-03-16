"""
Main module - game initialisation and flow
"""

import pygame

from graphics import easel
from game_component_database import ComponentDatabase
from game_component_factories import ComponentCollectionFactory
from player import Player
from settings import config
from buttons import ButtonCollection
from ai_simple import RandomAI
from game import game
from game_mechanics import GameMechanics


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

    game.init_game(
        players=players,
        buttons=ButtonCollection(),
        components=ComponentDatabase(),
        mechanics=GameMechanics()
    )

    # TODO: Move this initialisation into game.init_game
    # TODO: Remove dependency injection?
    game.mechanics.init_components(
        component_collection_factory=ComponentCollectionFactory()
    )

    # player[0] is the start player
    game.current_player = game.players[0]
    game.current_player.start()


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
                # ('Caroline', None),
                # ('Nigel', None),
                # ('Issie', None),
                # ('Coen', None),
                ('Caroline', RandomAI()),
                ('Nigel', RandomAI()),
                ('Issie', RandomAI()),
                ('Coen', None)
            ],
        )

        game.embody()

        # Notify main game loop that the initialisation is done
        self._running = True

    def on_event(self, event):
        """
        Process a pygame event
        :param event: the event
        """
        if event.type == pygame.QUIT:
            self._running = False

        # 'q' to quit - useful when running the game full screen
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self._running = False

        if event.type == pygame.MOUSEBUTTONUP:
            game.buttons.process_mouse_click(pygame.mouse.get_pos())

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
