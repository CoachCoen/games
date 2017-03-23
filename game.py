from settings import config
import pygame

from graphics import draw_table


class Game:
    """
    Container for game elements - components, players - and mechanics
    """
    def __init__(self):
        """
        Initialise an instance
        """
        self.components = None
        self._current_player = None
        self.buttons = None
        self.players = None
        self.mechanics = None
        self.finished = False

    def init_game(self, players, buttons, components, mechanics):
        """

        :param players: The 2, 3 or 4 players in the game
        :type players: list(player.Player)
        :param buttons: The active buttons
        :type buttons: button.ButtonCollection
        :param components: All the game pieces in the game, including in the
        supply, the holding areas and the players' areas
        :type components: game_component_database.ComponentDatabase
        :param mechanics: Calculates the valid moves, winner, score and
        other game mechanics
        :type mechanics: game_mechanics.GameMechanics
        """
        self.players = players
        self.components = components
        self.buttons = buttons
        self.mechanics = mechanics
        self.mechanics.init_components()

    @property
    def current_player(self):
        """
        :return: The active player
        :rtype: player.Player
        """
        return self._current_player

    @current_player.setter
    def current_player(self, player):
        """
        Sets _current_player and starts their turn

        :param player: The new active player
        :type player: player.Player
        """
        self._current_player = player
        player.start()

    @property
    def last_player(self):
        """
        Is the current player the last player in this round
        :return: True if this is the last player
        :rtype: bool
        """
        return self.current_player == self.players[-1]

    def embody(self):
        """
        Embody the game: draw the table top, the components and score, and
        create the buttons
        """
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

        # There can only be one card in the holding area
        for card in self.components.holding_area_cards:
            card.embody()

        for player in self.players:
            player.embody()

        pygame.display.flip()


game = Game()
