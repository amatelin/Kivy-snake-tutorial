import kivy
kivy.require('1.8.0')  # update with your current version

# import the kivy elements used by our classes
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class Playground(Widget):
    # children widgets containers
    fruit = ObjectProperty(None)
    snake = ObjectProperty(None)


class Fruit(Widget):
    pass


class Snake(Widget):
    # children widgets containers
    head = ObjectProperty(None)
    tail = ObjectProperty(None)


class SnakeHead(Widget):
    pass


class SnakeTail(Widget):
    pass


class SnakeApp(App):

    def build(self):
        game = Playground()
        return game

if __name__ == '__main__':
    SnakeApp().run()
