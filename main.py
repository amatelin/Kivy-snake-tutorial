import kivy
kivy.require('1.8.0')  # update with your current version

# import the kivy elements used by our classes
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import \
    ObjectProperty,  \
    NumericProperty, \
    ListProperty, \
    BooleanProperty, \
    OptionProperty, \
    ReferenceListProperty


class Playground(Widget):
    # children widgets containers
    fruit = ObjectProperty(None)
    snake = ObjectProperty(None)

    # grid parameters (chosent to respect the 16/9 format)
    col_number = 16
    row_number = 9

    # game variables
    score = NumericProperty(0)
    turn_counter = NumericProperty(0)
    fruit_rhythm = NumericProperty(0)

    # user input handling
    touch_start_pos = ListProperty()
    action_triggered = BooleanProperty(False)


class Fruit(Widget):
    # constants used to compute the fruit_rhythme
    # the values express a number of turns
    duration = NumericProperty(10)
    interval = NumericProperty(3)

    # representation on the canvas
    object_on_board = ObjectProperty(None)
    state = BooleanProperty(False)


class Snake(Widget):
    # children widgets containers
    head = ObjectProperty(None)
    tail = ObjectProperty(None)


class SnakeHead(Widget):
    # representation on the "grid" of the Playground
    direction = OptionProperty(
        "Right", options=["Up", "Down", "Left", "Right"])
    x_position = NumericProperty(0)
    y_position = NumericProperty(0)
    position = ReferenceListProperty(x_position, y_position)

    # representation on the canvas
    points = ListProperty([0] * 6)
    object_on_board = ObjectProperty(None)
    state = BooleanProperty(False)


class SnakeTail(Widget):
    # tail length, in number of blocks
    size = NumericProperty(3)

    # blocks positions on the Playground's grid
    blocks_positions = ListProperty()

    # blocks objects drawn on the canvas
    tail_blocks_objects = ListProperty()


class SnakeApp(App):
    game_engine = ObjectProperty(None)

    def build(self):
        self.game_engine = Playground()
        return self.game_engine

if __name__ == '__main__':
    SnakeApp().run()
