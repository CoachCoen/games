from drawing_surface import draw_rectangle, draw_pologon, draw_text, \
    draw_circle
from drawing_surface import ColourPalette, easel

CARD_WIDTH = 100
CARD_HEIGHT = 140

CARD_SPACING = 20

COLUMN_WIDTH = CARD_WIDTH + CARD_SPACING
ROW_HEIGHT = CARD_HEIGHT + CARD_SPACING

POINTS_LOCATION_X = 20
POINTS_LOCATION_Y = 10

COST_LOCATION_X = 20
COST_LOCATION_Y = 50

CHIP_SIZE = 20
CHIP_SPACING = 5

class AbstractDrawAction(object):
    pass


class DrawCardCost(AbstractDrawAction):
    def draw(self, x, y):
        # TODO Tidy layout
        for (i, (jewel_type, number)) in \
                enumerate([(jewel_type, number)
                           for (jewel_type, number)
                           in self.cost.items() if number]):
            location = (x, y + (i * (CHIP_SIZE + CHIP_SPACING)))
            draw_circle(location, CHIP_SIZE, jewel_type.value)

            location = (x + CHIP_SIZE, y + ((i - 0.3) * (CHIP_SIZE + CHIP_SPACING)))
            # TODO Choose a contrasting colour for the number
            draw_text(location, str(number), font_size=18)

class DrawCard(AbstractDrawAction):
    def draw(self, x, y):
        # draw_rectangle((x, y, x + CARD_WIDTH, y + CARD_HEIGHT),
        #                ColourPalette.card_background)
        draw_rectangle((x, y, CARD_WIDTH, CARD_HEIGHT),
                       ColourPalette.card_background)
        if self.points:
            draw_text((x + POINTS_LOCATION_X, y + POINTS_LOCATION_Y),
                      str(self.points))

        self.cost.draw(x + COST_LOCATION_X, y + COST_LOCATION_Y)

        # TODO Better variable name - top row?, top row left, top row right?
        draw_circle((x + CARD_WIDTH - POINTS_LOCATION_X,
                     int(y + POINTS_LOCATION_Y + CHIP_SIZE * 0.5)),
                    int(CHIP_SIZE * 1.5), self.jewel_type.value)


# class DrawCardDeck(AbstractDrawAction):
#     pass


class DrawCardRow(AbstractDrawAction):
    def draw(self, x, y):
        for column, card in enumerate(self.columns):
            card.draw(x + column * COLUMN_WIDTH, y)


class DrawCentralTableArea(AbstractDrawAction):
    def draw(self, x, y):
        for (i, card_row) in enumerate(self.card_rows):
            card_row.draw(x, y + i * ROW_HEIGHT)


class DrawTable(object):
    def _draw_tablecloth(self):
        draw_rectangle((0, 0, easel.width, easel.height),
                       ColourPalette.table_cloth)

    def _draw_player_corners(self):
        for (x, y) in [
            (0, 0),
            (0, easel.height),
            (easel.width, easel.height),
            (easel.width, 0)
        ]:
            draw_pologon([
                (x, abs(y - easel.height / 2.2)),
                (abs(x - easel.width / 2.2), y),
                (x, y)],
                ColourPalette.corners
            )

    def draw(self):
        self._draw_tablecloth()
        self._draw_player_corners()
        self.central_table_area.draw(380, 150)
        # self._draw_cards()
