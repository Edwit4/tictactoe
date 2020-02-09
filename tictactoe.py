import numpy as np
import kivy
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.app import App

kivy.require('1.11.1') # replace with your current kivy version !

class TicTacToeApp(App):
    def build(self):
        # Create tic tac toe game
        self.game = TicTacToeGame()

        # Create a rectangle to hold the game board
        self.game.bind(pos=self.update_rect, size=self.update_rect)

        # Add the image of the game board as the background of the
        # rectangle
        with self.game.canvas.before:
            self.rect = Rectangle(source='./images/grid.png',
                    size=self.game.size, pos=self.game.pos)

        return self.game

    # Update the size and position of the rectangle to follow the game
    # window
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class TicTacToeGame(BoxLayout):
    def __init__(self, **kwargs):
        super(TicTacToeGame, self).__init__(**kwargs)

        # Create a 3x3 grid of buttons.
        self.buttons = GridLayout(cols=3)
        for i in range(9):
            button_id = str(i)
            self.buttons.add_widget(PieceButton(source='./images/empty.png',
                on_press=self.update, id=button_id))
        self.add_widget(self.buttons)

        # Keep track of what turn it is
        self.turn = 0

        # Make a 3x3 grid of game pieces with vector representations
        # [0,0] represents empty square
        # [1,0] represents X
        # [0,1] represents O
        self.pieces = np.zeros((3,3,2))

    # Function to handle updating board on touch
    def update(self, instance):

        if instance.source == './images/empty.png':
            # First turn is X, then O, alternating each turn
            if self.turn % 2 == 0: 
                piece_type = 'X'
            else:
                piece_type = 'O'

            # Add image to board and keep track of which pieces are where
            piece = Piece(piece_type)
            instance.source = piece.image
            piece_index = int(instance.id)
            self.pieces = self.pieces.reshape((9,2))
            self.pieces[piece_index] = piece.rep
            self.pieces = self.pieces.reshape((3,3,2))

            # Check if somebody won (if a row / col / diag sums to 3 then
            # the whichever piece summed to 3 has won)
            col_sums = np.sum(self.pieces,axis=0)
            row_sums = np.sum(self.pieces,axis=1)
            diag_sums = np.array([np.trace(self.pieces), 
                    np.trace(np.flip(self.pieces,axis=0))])
            sums = np.concatenate([col_sums, row_sums, diag_sums])
            for vec in sums:
                if np.array_equal(vec, np.array([3,0])):
                    self.gameover('X wins')
                elif np.array_equal(vec, np.array([0,3])):
                    self.gameover('O wins')

            # If everything sums to 2 then there is a tie
            uniques, counts = np.unique(sums,return_counts=True)
            twos = np.isin(uniques,2)
            if np.any(twos):
                if counts[twos] == 8:
                    self.gameover('Tie')

            # Update the turn number
            self.turn += 1

    # If someone wins or the game is tied, restart
    def gameover(self, win_condition):
        self.remove_widget(self.buttons)
        TicTacToeApp().run()

# Custom button which has an image on it
class PieceButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(PieceButton, self).__init__(**kwargs)
        self.source = './images/empty.png'

# Class to hold the image and vector representation for each piece type
class Piece(Widget):

    def __init__(self, piece_type, **kwargs):
        super(Piece, self).__init__(**kwargs)

        # Depending on piece type load proper image and proper vector
        # representation
        if piece_type == 'X':
            self.image = './images/x.png'
            self.rep = np.array([1,0])
        elif piece_type == 'O':
            self.image = './images/o.png'
            self.rep = np.array([0,1])

