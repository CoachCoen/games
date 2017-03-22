from settings import config
import pygame

from graphics import draw_table


class Game:
    """
    Container for game elements - components, players - and mechanics
    """
    def __init__(self):
        self.components = None
        self._current_player = None
        self.buttons = None
        self.players = None
        self.mechanics = None
        self.finished = False

    def init_game(self, players, buttons, components, mechanics):
        self.players = players
        self.components = components
        self.buttons = buttons
        self.mechanics = mechanics
        self.mechanics.init_components()

    @property
    def current_player(self):
        return self._current_player

    @current_player.setter
    def current_player(self, player):
        self._current_player = player
        player.start()

    @property
    def last_player(self):
        return self.current_player == self.players[-1]

    def embody(self):
        game.buttons.reset()
        draw_table(self.mechanics.final_round)

        self.components.table_chips.embody()

        self.components.table_card_stacks.embody(
            location=config.central_area_location + config.card_decks_location
        )

        self.components.table_card_grid.embody()

        for tile in self.components.table_tiles.components:
            tile.embody()

        self.components.holding_area.embody()

        # There can only be one card in the holding area -
        # no need to specify a column
        for card in self.components.holding_area_cards:
            card.embody()

        for player in self.players:
            player.embody()

        pygame.display.flip()


game = Game()
