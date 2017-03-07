from settings import config
from vector import Vector
from chip_types import ChipType
from component_states import ComponentState
from states import PlayerStates

from drawing_surface import draw_rectangle, draw_text, \
    draw_circle, draw_card
from drawing_surface import ColourPalette, circle_location_to_rectangle

from game_actions import ReturnComponent, MoveComponentToHoldingArea, Cancel, Confirm

from states import ComponentStates

from buttons import buttons
from game_state import game
from game_actions import ToDo

VERTICAL = 0
HORIZONTAL = 1


class AbstractEmbodyMixin(object):
    pass
    # def embody(self, **kwargslocation=None, scaling_factor=1, **kwargs):
    #     """
    #     Show this component, plus any sub components,
    #     at the specified location and scaling factor
    #     If it can be clicked on, also add a button
    #     """
    #     self.buttonify()
    #     self.draw(location, scaling_factor)
    #
    # def buttonify(self):
    #     """
    #     To be overwritten for classes which can be clicked on
    #     """
    #     return NotImplemented
    #

class EmbodyChipStackMixin(AbstractEmbodyMixin):
    def embody(self):
        location = config.central_area_location + config.chip_stack_location
        for i, chip_type in enumerate(
                [c for c in ChipType if c in self.colour_count]
        ):
            chip_location = location + Vector(0, i * 2.5 * config.chip_size)

            chip = game.components.chip_from_supply(chip_type)
            # if chip in game.valid_actions or chip_type in game.valid_actions:

            # TODO: Tidy up passing in current player here?
            if game.components.is_valid_action(game.current_player, chip):
            # if chip in game.valid_actions._in(chip):
                buttons.add(
                    circle_location_to_rectangle(chip_location, config.chip_size),
                    ToDo([chip.to_holding_area, game.current_player.take_component])
                ).embody()

            draw_circle(chip_location, config.chip_size, chip_type)
            draw_text(location=chip_location - Vector(4, 6), text=str(self.colour_count[chip_type]),
                      text_colour=chip_type, reverse_colour=True)


class EmbodyChipCostMixin(AbstractEmbodyMixin):
    def embody(self, location):
            for i, chip_type in enumerate(
                    [c for c in ChipType if c in self.colour_count]
            ):
                chip_location = location + Vector(0, i * 2.5 * config.chip_size * config.chip_cost_scaling)

                draw_circle(chip_location, config.chip_size * config.chip_cost_scaling, chip_type)
                draw_text(location=chip_location - Vector(4, 6), text=str(self.colour_count[chip_type]),
                          text_colour=chip_type, reverse_colour=True)

#
# class EmbodyColourCountMixin(AbstractEmbodyMixin):
#     def embody(self, location, direction=VERTICAL, scaling_factor=1):
#         for i, chip_type in enumerate(
#                 [c for c in ChipType if c in self.colour_count]
#         ):
#             if direction == HORIZONTAL:
#                 chip_location = location + Vector(i * 2.5 * config.chip_size * scaling_factor, 0)
#             else:
#                 chip_location = location + Vector(0, i * 2.5 * config.chip_size * scaling_factor)
#
#             draw_circle(chip_location, config.chip_size * scaling_factor, chip_type)
#             draw_text(location=chip_location - Vector(4, 6), text=str(self.colour_count[chip_type]),
#                       text_colour=chip_type, reverse_colour=True)


class EmbodyTileMixin(AbstractEmbodyMixin):
    def embody(self):
        """
        Show this component, plus any sub components,
        at the specified location and scaling factor
        If it can be clicked on, also add a button
        """
        self.buttonify()
        self.draw()

    @property
    def location(self):
        if self.state == ComponentStates.in_supply:
            return config.central_area_location + \
                   config.tiles_row_location +\
                   Vector(self.column *
                          (config.tile_size.x + config.tile_spacing), 0)

    def draw(self):
        draw_rectangle(
            self.location.to_rectangle(config.tile_size),
            ColourPalette.card_background
        )
        draw_text(self.location + config.points_location,
                  str(self.points)
                  )
        self.chip_cost.embody(self.location + config.cost_location)

        # self.sub_components = [(
        #     chip_cost, config.cost_location, config.chip_cost_scaling
        # )]
        # self.location = None

    def buttonify(self):
        pass

    # def embody(self, location):
    #     self.location = location
    #     self._draw()
    #     self.chip_cost.embody(self.location + config.cost_location,
    #                           scaling_factor=config.chip_cost_scaling
    #                           )


class EmbodyChipMixin(AbstractEmbodyMixin):
    def __init__(self):
        self.column = None

    @property
    def location(self):
        # Individual chips are only show in the holding area - if not, raise an error
        assert self.state == ComponentStates.in_holding_area

        return config.holding_area_location + \
               config.holding_area_chips_location + \
               Vector(self.column * config.chip_size * 2.5, 0)

    def embody(self, column):
        self.column = column
        self.buttonify()
        self._draw()

    def buttonify(self):
        """
        If this chip can be moved, turn it into a button
        """
        # chip = game.components.chip_from_supply(chip_type)
        # if self in game.valid_actions:
        # Only embodied (as a single chip) if it is in the holding area
        # so always make it a button
        buttons.add(
            circle_location_to_rectangle(self.location, config.chip_size),
            ToDo([self.to_supply, game.current_player.return_component])
        ).embody()

        # if self in game.valid_actions:
        #     # If this is in the holding area, return it on click
        #     # otherwise move it to the holding area
        #     action = ReturnComponent(self) \
        #         if self.position == ComponentState.holding_area \
        #         else MoveComponentToHoldingArea(self)
        #
        #     # Create button and draw it (through embody() )
        #     buttons.add(
        #         circle_location_to_rectangle(
        #             self.location, config.chip_size * self.scaling_factor
        #         ),
        #         action
        #     ).embody()

    def _draw(self):
        """
        Draw the chip
        """
        draw_circle(
            self.location,
            int(config.chip_size),
            self.chip_type
        )


class EmbodyCardMixin(AbstractEmbodyMixin):
    def embody(self):
        """
        Show this component, plus any sub components,
        at the specified location and scaling factor
        If it can be clicked on, also add a button
        """
        self.buttonify()
        self.draw()

    @property
    def location(self):
        if self.face_up and self.state == ComponentStates.in_supply:
            return \
                config.card_decks_location + \
                config.central_area_location + \
                Vector(
                    (self.column + 1)* (config.card_size.x + config.card_spacing),
                    self.row * (config.card_size.y + config.card_spacing)
                )

        elif self.state == ComponentStates.in_holding_area:
            return config.holding_area_location + config.holding_area_card_location

        # column = self.column + 1 \
        #     if self.face_up and self.state == ComponentStates.in_supply \
        #     else 0
        # return \
        #     config.card_decks_location + \
        #     config.central_area_location +\
        #     Vector(
        #            column * (config.card_size.x + config.card_spacing),
        #            self.row * (config.card_size.y + config.card_spacing)
        #     )

    def buttonify(self):
        """
        Turn the card into a 'button' so the user can click on it
        """
        # If currently in supply - move it to the holding area
        if self.state == ComponentStates.in_supply and self in game.valid_actions:
            buttons.add(
                self.location.to_rectangle(config.card_size),
                ToDo([self.to_holding_area, game.current_player.take_component])
            ).embody()
        elif self.state == ComponentStates.in_holding_area:
            buttons.add(
                self.location.to_rectangle(config.card_size),
                ToDo([self.move_back, game.current_player.return_component])
            ).embody()

        # If currently in holding area - return to the previous location

        # If currently reserved - move it to the holding area




            # ToDo([self.to_supply, game.current_player.return_component])
            #
            #
            #
            # # If in holding area, return the card
            # # otherwise, take the card
            # action = ReturnComponent(self) \
            #     if self.position == ComponentState.holding_area \
            #     else MoveComponentToHoldingArea(self)
            #
            # # Create button, add to list, and draw a line around
            # # the card, to show it can be taken
            # buttons.add(
            #     self.location.to_rectangle(config.card_size),
            #     action
            # ).embody()

    def draw(self):
        """
        Draw the rectangle and the value (points)
        The cost (chips) and resulting chip types
        will draw themselves
        """
        draw_card(self.location)
        if self.points:
            draw_text(
                self.location + config.points_location,
                str(self.points)
            )

        draw_circle(self.location + config.reward_chip_location,
                    config.chip_size * config.reward_chip_scaling,
                    self.chip_type)

        self.chip_cost.embody(self.location + config.cost_location)


class EmbodyCardGridMixin(AbstractEmbodyMixin):
    def embody(self):
        for row in self.card_grid:
            for card in row:
                if card:
                    card.embody()


class EmbodyCardDeckCountMixin(AbstractEmbodyMixin):
    def embody(self, location):
        for row in range(3):
            if self.card_deck_count[row]:
                deck_location = location + \
                                Vector(0, row * (config.card_size.y + config.card_spacing))
                draw_rectangle(deck_location.to_rectangle(config.card_size),
                               ColourPalette.card_deck_background)
                draw_text(
                    deck_location + config.points_location,
                    str(self.card_deck_count[row])
                )


def _embody_holding_area():
    _draw_holding_area()

    buttons.add(
        (
            config.holding_area_location + config.cancel_button_location
        ).to_rectangle(config.button_size),
        Cancel(),
        text='Cancel'
    ).embody()

    # if game.is_turn_complete:
    # TODO: Import & use VALID
    if game.components.turn_complete(game.current_player):
        buttons.add(
            (
                config.holding_area_location + config.confirm_button_location
            ).to_rectangle(config.button_size),
            Confirm(),
            text='Confirm'
        ).embody()


def _draw_holding_area():
    draw_rectangle(
        config.holding_area_location.to_rectangle(
            config.holding_area_size
        ),
        ColourPalette.holding_area
    )

    draw_text(
        config.holding_area_location +
        config.holding_area_name_location,
        text=game.current_player.name
    )


class EmbodyPlayerMixin(AbstractEmbodyMixin):
    def embody(self):
        self._draw()
        game.components.chip_count_for_player(self).embody(self)
        game.components.card_reward_for_player(self).embody(self)
        # chip_counts = self.chips.counts_for_type
        # card_counts = self.cards.counts_for_type
        # draw_circles_row(
        #     config.player_chip_stack_location,
        #     chip_counts,
        #     player_order=self.player_order
        # )
        # draw_squares_row(
        #     config.player_card_deck_location,
        #     card_counts,
        #     player_order=self.player_order
        # )
        # self.reserved.embody(config.player_reserved_location,
        #                      player_order=self.player_order)

    # TODO: Refactor this - messy?
    def _draw(self):
        draw_rectangle(
            (0, 0, config.player_area_size.x, config.player_area_size.y),
            player_order=self.player_order,
            colour=ColourPalette.active_player_area
            if self.state != PlayerStates.player_waiting
            else ColourPalette.player_area
        )
        draw_text(
            (config.player_name_location.x, config.player_name_location.y),
            self.name,
            player_order=self.player_order
        )
        # if self.points:
        #     draw_text(
        #         (config.player_points_location.x,
        #          config.player_points_location.y),
        #         str(self.points),
        #         player_order=self.player_order
        #     )



class EmbodyComponentDatabaseMixin(AbstractEmbodyMixin):
    def embody(self):
        self.table_chips.embody()

        self.table_card_stacks.embody(
            location=config.central_area_location + config.card_decks_location
        )

        self.table_card_grid.embody()

        for tile in self.table_tiles.components:
            tile.embody()

        holding_area_components = self.holding_area_components
        if len(holding_area_components):
            _embody_holding_area()
        for i, chip in enumerate(self.holding_area_chips):
            chip.embody(column=i)

        # There can only be one card in the holding area - no need to specify a column
        for card in self.holding_area_cards:
            card.embody()

        for player in game.players:
            player.embody()


class EmbodyPlayerChipStack(AbstractEmbodyMixin):
    # TODO: Lots of overlap with other chip count/stack embody methods
    def embody(self, player):
        for i, chip_type in enumerate(
                [c for c in ChipType if c in self.colour_count]
        ):
            if self.colour_count[chip_type]:
                chip_location = config.player_chip_stack_location \
                                + Vector(i * 2.5 * config.player_chip_stack_scaling * config.chip_size, 0)

                draw_circle(
                    chip_location,
                    config.chip_size * config.player_chip_stack_scaling,
                    chip_type,
                    player_order=player.player_order,
                )
                draw_text(
                    location=chip_location - Vector(4, 6),
                    text=str(self.colour_count[chip_type]),
                    text_colour=chip_type,
                    reverse_colour=True,
                    player_order=player.player_order,

                )


class EmbodyPlayerCardStack(AbstractEmbodyMixin):
    # TODO: Lots of overlap with other chip count/stack embody methods
    def embody(self, player):
        for i, chip_type in enumerate(
                [c for c in ChipType if c in self.colour_count]
        ):
            if self.colour_count[chip_type]:
                location = config.player_card_deck_location \
                                + Vector(i * 2.5 * config.player_chip_stack_scaling * config.chip_size, 0)

                draw_rectangle(
                    location.to_rectangle(Vector(2 * config.chip_size * config.player_chip_stack_scaling, config.chip_size * config.player_chip_stack_scaling * 2)),
                    chip_type,
                    player_order=player.player_order,
                )
                draw_text(
                    location=location - Vector(4, 6),
                    text=str(self.colour_count[chip_type]),
                    text_colour=chip_type,
                    reverse_colour=True,
                    player_order=player.player_order,

                )
