from settings import config
from vector import Vector
from chip_types import ChipType
from component_states import ComponentState

from drawing_surface import draw_rectangle, draw_text, \
    draw_circle, draw_card
from drawing_surface import ColourPalette, circle_location_to_rectangle

from game_actions import ReturnComponent, MoveComponentToHoldingArea

from states import ComponentStates

from buttons import buttons
from game_state import game
from game_actions import Move

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

            if chip_type in game.valid_actions:
                chip = game.components.chip_from_supply(chip_type)
                buttons.add(
                    circle_location_to_rectangle(chip_location, config.chip_size),
                    Move(chip.to_holding_area)
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
    def buttonify(self):
        """
        If this chip can be moved, turn it into a button
        """
        if self in game.valid_actions:
            # If this is in the holding area, return it on click
            # otherwise move it to the holding area
            action = ReturnComponent(self) \
                if self.position == ComponentState.holding_area \
                else MoveComponentToHoldingArea(self)

            # Create button and draw it (through embody() )
            buttons.add(
                circle_location_to_rectangle(
                    self.location, config.chip_size * self.scaling_factor
                ),
                action
            ).embody()

    def _draw(self):
        """
        Draw the chip
        """
        draw_circle(
            self.location,
            int(config.chip_size * self.scaling_factor),
            self.chip_type,
            player_order=self.player_order
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
        column = self.column + 1 \
            if self.face_up and self.state == ComponentStates.in_supply \
            else 0
        return \
            config.card_decks_location + \
            config.central_area_location +\
            Vector(
                   column * (config.card_size.x + config.card_spacing),
                   self.row * (config.card_size.y + config.card_spacing)
            )

    def buttonify(self):
        """
        Turn the card into a 'button' so the user can click on it
        """
        if self in game.valid_actions:
            # If in holding area, return the card
            # otherwise, take the card
            action = ReturnComponent(self) \
                if self.position == ComponentState.holding_area \
                else MoveComponentToHoldingArea(self)

            # Create button, add to list, and draw a line around
            # the card, to show it can be taken
            buttons.add(
                self.location.to_rectangle(config.card_size),
                action
            ).embody()

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

class EmbodyComponentDatabaseMixin(AbstractEmbodyMixin):
    def embody(self):
        self.table_chips.embody()

        self.table_card_stacks.embody(
            location=config.central_area_location + config.card_decks_location
        )

        self.card_grid.embody()
        # location=
        #                       config.central_area_location +
        #                       config.card_decks_location +
        #                       Vector(config.card_size.x + config.card_spacing, 0)
        #                       )
        #
        for tile in self.table_tiles.components:
            tile.embody()
