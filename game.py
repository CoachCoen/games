"""
Main module - game initialisation and flow
"""

import pygame

from drawing_surface import easel
from game_objects import Table, HoldingArea
from player import Player
from settings import config
from buttons import buttons
from ai_simple import RandomAI
from game_state import game


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
        table=Table(len(players)),
        holding_area=HoldingArea(),
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
            (0, 0),
            pygame.HWSURFACE | pygame.DOUBLEBUF
        ) # | pygame.FULLSCREEN
        config.scaling_factor = pygame.display.Info().current_w / 1366.0
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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self._running = False
        if event.type == pygame.MOUSEBUTTONUP:
            game.buttons.process_mouse_click()

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
