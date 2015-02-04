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
from kivy.graphics import Triangle, Rectangle, Ellipse
from kivy.vector import Vector
from random import randint


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

    def start(self):
        # draw new snake on board
        self.new_snake()

        # start update loop
        self.update()

    def reset(self):
        # reset game variables
        self.turn_counter = 0
        self.score = 0

        # remove the snake widget and the fruit if need be; its remove method
        # will make sure that nothing bad happens anyway
        self.snake.remove()
        self.fruit.remove()

    def new_snake(self):
        # generate random coordinates
        start_coord = (
            randint(2, self.col_number - 2), randint(2, self.row_number - 2))

        # set random coordinates as starting position for the snake
        self.snake.set_position(start_coord)

        # generate random direction
        rand_index = randint(0, 3)
        start_direction = ["Up", "Down", "Left", "Right"][rand_index]

        # set random direction as starting direction for the snake
        self.snake.set_direction(start_direction)

    def pop_fruit(self, *args):
        # get random coordinates for the fruit
        random_coord = [
            randint(1, self.col_number), randint(1, self.row_number)]

        # get all cells positions occupied by the snake
        snake_space = self.snake.get_full_position()

        # if the coordinates are on a cell occupied by the snake, re-draw
        while random_coord in snake_space:
            random_coord = [
                randint(1, self.col_number), randint(1, self.row_number)]

        # pop fruit widget on the coordinates generated
        self.fruit.pop(random_coord)

    def is_defeated(self):
        """
        Used to check if the current snake position corresponds to a defeat.
        """
        snake_position = self.snake.get_position()

        # if the snake bites its own tail : defeat
        if snake_position in self.snake.tail.blocks_positions:
            return True

        # if the snake it out of the board : defeat
        if snake_position[0] > self.col_number \
                or snake_position[0] < 1 \
                or snake_position[1] > self.row_number \
                or snake_position[1] < 1:
            return True

        return False

    def update(self, *args):
        """
        Used to make the game progress to a new turn.
        """
        # move snake to its next position
        self.snake.move()

        # check for defeat
        # if it happens to be the case, reset and restart game
        if self.is_defeated():
            self.reset()
            self.start()
            return

        # check if the fruit is being eaten
        if self.fruit.is_on_board():
            # if so, remove the fruit, increment score and tail size
            if self.snake.get_position() == self.fruit.pos:
                self.fruit.remove()
                self.score += 1
                self.snake.tail.size += 1

        # increment turn counter
        self.turn_counter += 1

    def on_touch_down(self, touch):
        self.touch_start_pos = touch.spos

    def on_touch_move(self, touch):
        # compute the translation from the start position
        # to the current position
        delta = Vector(*touch.spos) - Vector(*self.touch_start_pos)

        # check if a command wasn't already sent and if the translation
        # is > to 10% of the screen's size
        if not self.action_triggered \
                and (abs(delta[0]) > 0.1 or abs(delta[1]) > 0.1):
            # if so, set the appropriate direction to the snake
            if abs(delta[0]) > abs(delta[1]):
                if delta[0] > 0:
                    self.snake.set_direction("Right")
                else:
                    self.snake.set_direction("Left")
            else:
                if delta[1] > 0:
                    self.snake.set_direction("Up")
                else:
                    self.snake.set_direction("Down")
            # register that an action was triggered so that
            # it doesn't happen twice during the same turn
            self.action_triggered = True

    def on_touch_up(self, touch):
        # we're ready to accept a new instruction
        self.action_triggered = False


class Fruit(Widget):
    # constants used to compute the fruit_rhythme
    # the values express a number of turns
    duration = NumericProperty(10)
    interval = NumericProperty(3)

    # representation on the canvas
    object_on_board = ObjectProperty(None)
    state = BooleanProperty(False)

    def is_on_board(self):
        return self.state

    def remove(self, *args):
        # we accept *args because this method will be passed to an
        # event dispatcher so it will receive a dt argument.
        if self.is_on_board():
            self.canvas.remove(self.object_on_board)
            self.object_on_board = ObjectProperty(None)
            self.state = False

    def pop(self, pos):
        self.pos = pos  # used to check if the fruit is begin eaten

        # drawing the fruit
        # (which is just a circle btw, so I guess it's an apple)
        with self.canvas:
            x = (pos[0] - 1) * self.size[0]
            y = (pos[1] - 1) * self.size[1]
            coord = (x, y)

            # storing the representation and update the state of the object
            self.object_on_board = Ellipse(pos=coord, size=self.size)
            self.state = True


class Snake(Widget):
    # children widgets containers
    head = ObjectProperty(None)
    tail = ObjectProperty(None)

    def move(self):
        """
        Moving the snake involves 3 steps :
            - save the current head position, since it will be used to add a
            block to the tail.
            - move the head one cell in the current direction.
            - add the new tail block to the tail.
        """
        next_tail_pos = list(self.head.position)
        self.head.move()
        self.tail.add_block(next_tail_pos)

    def remove(self):
        """
        With our current snake, removing the whole thing sums up to remove its
        head and tail, so we just have to call the corresponding methods. How
        they deal with it is their problem, not the Snake's. It just passes
        down the command.
        """
        self.head.remove()
        self.tail.remove()

    def set_position(self, position):
        self.head.position = position

    def get_position(self):
        """
        We consider the Snake's position as the position occupied by the head.
        """
        return self.head.position

    def get_full_position(self):
        """
        But sometimes we'll want to know the whole set of cells occupied by
         the snake.
        """
        return self.head.position + self.tail.blocks_positions

    def set_direction(self, direction):
        self.head.direction = direction

    def get_direction(self):
        return self.head.direction


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

    def is_on_board(self):
        return self.state

    def remove(self):
        if self.is_on_board():
            self.canvas.remove(self.object_on_board)
            self.object_on_board = ObjectProperty(None)
            self.state = False

    def show(self):
        """
        Actual rendering of the snake's head. The representation is simply a
        Triangle oriented according to the direction of the object.
        """
        with self.canvas:
            if not self.is_on_board():
                self.object_on_board = Triangle(points=self.points)
                self.state = True  # object is on board
            else:
                # if object is already on board, remove old representation
                # before drawing a new one
                self.canvas.remove(self.object_on_board)
                self.object_on_board = Triangle(points=self.points)

    def move(self):
        """
        Let's agree that this solution is not very elegant. But it works.
        The position is updated according to the current direction. A set of
        points representing a Triangle turned toward the object's direction is
        computed and stored as property.
        The show() method is then called to render the Triangle.
        """
        if self.direction == "Right":
            # updating the position
            self.position[0] += 1

            # computing the set of points
            x0 = self.position[0] * self.width
            y0 = (self.position[1] - 0.5) * self.height
            x1 = x0 - self.width
            y1 = y0 + self.height / 2
            x2 = x0 - self.width
            y2 = y0 - self.height / 2
        elif self.direction == "Left":
            self.position[0] -= 1
            x0 = (self.position[0] - 1) * self.width
            y0 = (self.position[1] - 0.5) * self.height
            x1 = x0 + self.width
            y1 = y0 - self.height / 2
            x2 = x0 + self.width
            y2 = y0 + self.height / 2
        elif self.direction == "Up":
            self.position[1] += 1
            x0 = (self.position[0] - 0.5) * self.width
            y0 = self.position[1] * self.height
            x1 = x0 - self.width / 2
            y1 = y0 - self.height
            x2 = x0 + self.width / 2
            y2 = y0 - self.height
        elif self.direction == "Down":
            self.position[1] -= 1
            x0 = (self.position[0] - 0.5) * self.width
            y0 = (self.position[1] - 1) * self.height
            x1 = x0 + self.width / 2
            y1 = y0 + self.height
            x2 = x0 - self.width / 2
            y2 = y0 + self.height

        # storing the points as property
        self.points = [x0, y0, x1, y1, x2, y2]

        # rendering the Triangle
        self.show()


class SnakeTail(Widget):
    # tail length, in number of blocks
    size = NumericProperty(3)

    # blocks positions on the Playground's grid
    blocks_positions = ListProperty()

    # blocks objects drawn on the canvas
    tail_blocks_objects = ListProperty()

    def remove(self):
        # reset the size if some fruits were eaten
        self.size = 3

        # remove every block of the tail from the canvas
        # this is why we don't need a is_on_board() here :
        # if a block is not on board, it's not on the list
        # thus we can't try to delete an object not already
        # drawn
        for block in self.tail_blocks_objects:
            self.canvas.remove(block)

        # empty the lists containing the blocks coordinates
        # and representations on the canvas
        self.blocks_positions = []
        self.tail_blocks_objects = []

    def add_block(self, pos):
        """
        3 things happen here :
            - the new block position passed as argument is appended to the
            object's list.
            - the list's number of elements is adapted if need be by poping
            the oldest block.
            - the blocks are drawn on the canvas, and the same process as before
            happens so that our list of block objects keeps a constant size.
        """
        # add new block position to the list
        self.blocks_positions.append(pos)

        # control number of blocks in the list
        if len(self.blocks_positions) > self.size:
            self.blocks_positions.pop(0)

        with self.canvas:
            # draw blocks according to the positions stored in the list
            for block_pos in self.blocks_positions:
                x = (block_pos[0] - 1) * self.width
                y = (block_pos[1] - 1) * self.height
                coord = (x, y)
                block = Rectangle(pos=coord, size=(self.width, self.height))

                # add new block object to the list
                self.tail_blocks_objects.append(block)

                # control number of blocks in list and remove from the canvas
                # if necessary
                if len(self.tail_blocks_objects) > self.size:
                    last_block = self.tail_blocks_objects.pop(0)
                    self.canvas.remove(last_block)


class SnakeApp(App):
    game_engine = ObjectProperty(None)

    def build(self):
        self.game_engine = Playground()
        return self.game_engine

if __name__ == '__main__':
    SnakeApp().run()
