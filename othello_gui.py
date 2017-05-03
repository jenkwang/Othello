#Jenny Chong 23733553 Lab Section 8

import othello_game_logic
import tkinter
from tkinter import messagebox
import SetBoard
import HowToPlay

DEFAULT_FONT = ('Arial', 15)
   
class OthelloApplication:
    def __init__(self):
        self._root_window = tkinter.Tk()
        
        self._start_button = tkinter.Button(
            master = self._root_window, text = 'Start Game', font = DEFAULT_FONT,
            width = 10,
            command = self._start_button_clicked)
        
        self._start_button.pack()

        self._how_to_button = tkinter.Button(
            master = self._root_window,
            text = 'How to Play', font = DEFAULT_FONT,
            width = 10,
            command = self._how_to_play_clicked)
        
        self._how_to_button.pack()

        self._quit_button = tkinter.Button(
            master = self._root_window, text = 'Quit', font = DEFAULT_FONT,
            width = 10,
            command = self._quit_button_clicked)

        self._quit_button.pack()

        self._root_window.rowconfigure(0, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)

    def run(self) -> None:
        self._root_window.mainloop()

    def _start_button_clicked(self) -> None:
        setboard = SetBoard.SetBoard()
        setboard.show()
                
    def _how_to_play_clicked(self) -> None:
        howtoplay = HowToPlay.HowToPlay()
        howtoplay.show()

    def _quit_button_clicked(self) -> None:
        self._root_window.destroy()


if __name__ == '__main__':
    OthelloApplication().run()
        
        
