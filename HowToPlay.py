#Jenny Chong 23733553 Lab Section 8

import tkinter

DEFAULT_FONT = ('Arial', 12)

class HowToPlay:
    def __init__(self):
        self._how_to_play_window = tkinter.Toplevel()

        self._how_to_play_window.resizable(width = False, height = False)
        
        self._instructions_label = tkinter.Label(master = self._how_to_play_window,
        text=
        """
        HOW TO PLAY
        
        Initializing the board:
        -rows and columns must be and even integer between 4 and 16
        -players can decide how the board will start off
        -players can decide which color goes first
        -players can decide how the game is won

        Playing the Game:
        -the player starting must place their piece in a position where
        one or more of the opponent's piece(s) is occupied between two
        of the player's pieces (in any of the 8 directions)
        -after placing their piece, all of their opponent's pieces between
        their two pieces will flip to their color
        -the turns will switch and the same concept applies until both
        players are unable to make a move or if the board is full
        -if a player is unable to make a move the turn will automatically
        swith to the opposite side
        """, font = DEFAULT_FONT, justify = tkinter.LEFT)

        self._instructions_label.grid(
            row = 0, column = 0, padx = 10, pady = 10)

        button_frame = tkinter.Frame(master = self._how_to_play_window)

        button_frame.grid(
            row = 1, column = 0, padx = 10, pady = 10)

        self._back_button = tkinter.Button(
            master = button_frame,
            text = "Back", font = DEFAULT_FONT,
            command = self._back_button_clicked)

        self._back_button.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.E)

        self._how_to_play_window.rowconfigure(0, weight = 1)
        self._how_to_play_window.rowconfigure(1, weight = 1)
        self._how_to_play_window.columnconfigure(0, weight = 1)

    def show(self) -> None:
        self._how_to_play_window.grab_set()
        self._how_to_play_window.wait_window()

    def _back_button_clicked(self) -> None:
        self._how_to_play_window.destroy()
