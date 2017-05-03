#Jenny Chong 23733553 Lab Section 8

import tkinter
from tkinter import messagebox
import othello_game_logic
import PlayGame

DEFAULT_FONT = ('Arial', 15)

class SetBoard:
    def __init__(self):
        self._set_board_window = tkinter.Toplevel()

        self._set_board_window.resizable(width = False, height = False)

        self._row_var = tkinter.IntVar()

        self._col_var = tkinter.IntVar()

        size_label = tkinter.Label(
            master = self._set_board_window, text = 'Please set up the empty board',
            font = DEFAULT_FONT)

        size_label.grid(
            row = 0, column = 0, columnspan = 3, padx = 10, pady = 10,
            sticky = tkinter.W)

        row_label = tkinter.Label(
            master = self._set_board_window, text = 'Rows:',
            font = ('Arial', 10))

        row_label.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        column_label = tkinter.Label(
            master = self._set_board_window, text = 'Columns:',
            font = ('Arial', 10))

        column_label.grid(
            row = 3, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        turn_label = tkinter.Label(
            master = self._set_board_window, text = 'Starting Player:',
            font = ('Arial', 10))

        turn_label.grid(
            row = 5, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        win_method_label = tkinter.Label(
            master = self._set_board_window, text = 'How to win:',
            font = ('Arial', 10))

        win_method_label.grid(
            row = 6, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        button_frame = tkinter.Frame(master = self._set_board_window)

        button_frame.grid(
            row = 7, column = 0, columnspan = 4, padx = 10, pady = 10,
            sticky = tkinter.E + tkinter.S)

        ok_button = tkinter.Button(
            master = button_frame, text = 'Confirm', font = ('Arial', 15),
            command = self._on_ok_button, height = 1, width = 10)

        ok_button.grid(row = 7, column = 0, padx = 10, pady = 10, sticky = tkinter.W)

        back_button = tkinter.Button(
            master = button_frame, text = 'Cancel', font = ('Arial', 15),
            command = self._on_back_button, height = 1, width = 10)

        back_button.grid(row = 7, column = 2, padx = 10, pady = 10, sticky = tkinter.E)

        self._set_board_window.rowconfigure(0, weight = 1)
        self._set_board_window.rowconfigure(1, weight = 1)
        self._set_board_window.rowconfigure(2, weight = 1)
        self._set_board_window.rowconfigure(3, weight = 1)
        self._set_board_window.rowconfigure(4, weight = 1)
        self._set_board_window.rowconfigure(5, weight = 1)
        self._set_board_window.rowconfigure(6, weight = 1)
        self._set_board_window.rowconfigure(7, weight = 1)
        self._set_board_window.columnconfigure(0, weight = 1)
        self._set_board_window.columnconfigure(1, weight = 1, uniform = 'uni')
        self._set_board_window.columnconfigure(2, weight = 1, uniform = 'uni')
        self._set_board_window.columnconfigure(3, weight = 1, uniform = 'uni')

        self._ok_clicked = False
        self.create_row_col_options(1, self._row_var)
        self.create_row_col_options(3, self._col_var)
        self.create_starting_player_option()
        self.create_how_to_win_option()

    def show(self) -> None:
        self._set_board_window.grab_set()
        self._set_board_window.wait_window()

    def create_row_col_options(self, start: int, var: 'idk') -> None:
        numbers = [
            ('4',4),('6',6),('8',8),
            ('10',10),('12',12),('14',14),('16',16)
        ]
        var.set(8)
        r = start
        c = 1
        if c < 5:
            for txt, val in numbers[0:3]:
                tkinter.Radiobutton(master = self._set_board_window, 
                            text=txt,
                            padx = 10,
                            variable = var,
                            value=val).grid(row=r,column=c)
                c += 1
            else:
                c = 1
                r = start + 1
                for txt, val in numbers[4:]:
                    tkinter.Radiobutton(master = self._set_board_window, 
                                text=txt,
                                padx = 10,
                                variable = var,
                                value=val).grid(row=r,column=c)
                    c += 1
                
    def create_starting_player_option(self) -> None:
        colors = [
            ('Black', 'B'), ('White', 'W')
        ]
        self._color_var = tkinter.StringVar()
        self._color_var.set('B')
        c = 1
        for txt, val in colors:
            tkinter.Radiobutton(master = self._set_board_window, 
                        text=txt,
                        padx = 10, 
                        variable = self._color_var,
                        value=val).grid(row=5,column=c)
            c += 1

    def create_how_to_win_option(self) -> None:
        options = [
            ('Most pieces', '>'), ('Least pieces', '<')
        ]
        self._option_var = tkinter.StringVar()
        self._option_var.set('>')
        c = 1
        for txt, val in options:
            tkinter.Radiobutton(master = self._set_board_window, 
                        text=txt,
                        padx = 10, 
                        variable = self._option_var,
                        value=val).grid(row=6,column=c)
            c += 1
        
    def was_ok_clicked(self) -> bool:
        return self._ok_clicked

    def _on_ok_button(self) -> None:
        self._ok_clicked = True
        self._rows = self._row_var.get()
        self._columns = self._col_var.get()
        self._turn = self._color_var.get()
        self._win_type = self._option_var.get()
        
        gamestate = othello_game_logic.GameState(self._rows, self._columns, self._turn, self._win_type)
        
        self._set_board_window.destroy()

        playgame = PlayGame.PlayGame(gamestate)
        playgame.show()

    def _on_back_button(self) -> None:
        self._set_board_window.destroy()

        
