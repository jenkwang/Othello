#Jenny Chong 23733553 Lab Section 8
#Point, Spot, and Spotstate class is what happens behind
#PlayGame class is what the user sees

import tkinter
from tkinter import messagebox
import SetBoard
import othello_game_logic
import math

DEFAULT_FONT = ('Arial', 15)

class Point:
    def __init__(self, frac_x: float, frac_y: float):
        self._frac_x = frac_x
        self._frac_y = frac_y
        
    def frac(self) -> (float, float):
        return (self._frac_x, self._frac_y)

    def pixel(self, pixel_width: float, pixel_height: float) -> (float, float):
        return(self._frac_x * pixel_width, self._frac_y * pixel_height)

    def frac_distance_from(self, p: 'Point') -> float:
        x = (self._frac_x - p._frac_x)
        y = (self._frac_y - p._frac_y)
        return math.hypot(x, y)

def from_frac(frac_x: float, frac_y: float) -> Point:
    return Point(frac_x, frac_y)

def from_pixel(pixel_x: float, pixel_y: float, pixel_width: float, pixel_height: float) -> Point:
    return Point(pixel_x / pixel_width, pixel_y / pixel_height)


class Spot:
    def __init__(self, center: 'Point', radius_frac: float):
        self._center = center
        self._radius_frac = radius_frac

    def center(self) -> 'Point':
        '''Returns a Point object representing piece's center'''
        return self._center

    def radius_frac(self) -> float:
        '''Returns the radius of this piece (frac)'''
        return self._radius_frac

    def contains(self, point: 'Point') -> bool:
        '''Checks if given Point object is within a piece'''
        return self._center.frac_distance_from(point) <= self._radius_frac


class SpotsState:
    def __init__(self):
        self._spots = []

    def all_spots(self) -> [Spot]:
        '''Returns a list of player's pieces'''
        return self._spots

    def handle_click(self, click_point: 'Point', radius:int) -> None:
        '''Handles click by either placing or removing a piece'''

        for i in reversed(range(len(self._spots))):
            if self._spots[i].contains(click_point):
                del self._spots[i]
                return

        self._spots.append(Spot(click_point, radius))

    def clear(self) -> None:
        self._spots = []


class PlayGame:
    def __init__(self, gamestate: 'GameState'):
        self._play_window = tkinter.Toplevel()

        self._black_pieces = SpotsState()
        self._black = []

        self._white_pieces = SpotsState()
        self._white = []
        
        self._gamestate = gamestate
        
        self._canvas = tkinter.Canvas(
            master = self._play_window, width = 500, height = 500,
            background = '#CCFFCC', highlightbackground = 'white')

        self._canvas.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)

        self._first_player = tkinter.Button(
            master = self._play_window,
            text = (gamestate._turn + ' is ready'), font = DEFAULT_FONT,
            command = self._first_player_clicked)

        self._first_player.grid(
            row = 0, column = 0, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        ready = tkinter.messagebox.showinfo("Ready?", ('Player 1 please place initial pieces before clicking Ready'))
            
        self._play_window.rowconfigure(0, weight = 1)
        self._play_window.rowconfigure(1, weight = 1)
        self._play_window.rowconfigure(2, weight = 1)
        self._play_window.columnconfigure(0, weight = 1)
        
    def show(self) -> None:
        self._play_window.grab_set()
        self._play_window.wait_window()

    def _on_canvas_clicked(self, event: tkinter.Event) -> None:
        '''Places the designated piece when canvas is clicked'''
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        width_spacing = width / self._gamestate._columns
        height_spacing = height / self._gamestate._rows

        self._move = [0,0]
        self._radiusx = (width_spacing / 2) / width
        self._radiusy = (height_spacing / 2) / height

        for row in range(self._gamestate._rows):
            if event.y in range(int(height_spacing*(row)), int(height_spacing*(row+1))):
                for col in range(self._gamestate._columns):
                    if event.x in range(int(width_spacing*(col)), int(width_spacing*(col+1))):
                        click_point = from_pixel((((col+1)*width_spacing)-(width_spacing/2)),
                            (((row+1)*height_spacing)-(height_spacing/2)), width, height)
                        self._move = [row, col]
                        
        if self._gamestate._turn == 'B':
            if self._gamestate._board[self._move[0]][self._move[1]] == 0:
                self._black_pieces.handle_click(click_point, self._radiusx)
                self._gamestate._board[self._move[0]][self._move[1]] = 'B'
            elif self._gamestate._board[self._move[0]][self._move[1]] == 'B':
                self._black_pieces.handle_click(click_point, self._radiusx)
                self._gamestate._board[self._move[0]][self._move[1]] = 0
                        
        elif self._gamestate._turn == 'W':
            if self._gamestate._board[self._move[0]][self._move[1]] == 0:
                self._white_pieces.handle_click(click_point, self._radiusx)
                self._gamestate._board[self._move[0]][self._move[1]] = 'W'
            elif self._gamestate._board[self._move[0]][self._move[1]] == 'W':
                self._white_pieces.handle_click(click_point, self._radiusx)
                self._gamestate._board[self._move[0]][self._move[1]] = 0
            elif self._gamestate._board[self._move[0]][self._move[1]] == 'B':
                pass

        self.redraw_board()

    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        self.redraw_board()

    def redraw_board(self):
        '''Redraws the board after time the window size changes'''
        self._canvas.delete(tkinter.ALL)

        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        
        width_spacing = width / self._gamestate._columns
        height_spacing = height / self._gamestate._rows
        
        for row in range(self._gamestate._rows):
            y1=int((row+1) * height_spacing)
            x2=int(width)
            y2=int((row+1) * height_spacing)
            
            self._canvas.create_line(0, y1, x2, y2, fill = "black")
            
        for col in range(self._gamestate._columns):
            x1 = int((col+1) * width_spacing)
            x2 = int((col+1) * width_spacing)
            y2 = int(height)
            
            self._canvas.create_line(x1, 0, x2, y2, fill = "black")
            
        for black in self._black_pieces.all_spots():
            center_x, center_y = black.center().pixel(width, height)

            radius_x = black.radius_frac() * width
            radius_y = self._radiusy * height
            
            self._canvas.create_oval(
                center_x - radius_x, center_y - radius_y,
                center_x + radius_x, center_y + radius_y,
                fill = 'black', outline = '#000000')
            
        for white in self._white_pieces.all_spots():
            center_x, center_y = white.center().pixel(width, height)

            radius_x = white.radius_frac() * width
            radius_y = self._radiusy * height
            
            self._canvas.create_oval(
                center_x - radius_x, center_y - radius_y,
                center_x + radius_x, center_y + radius_y,
                fill = 'white', outline = '#000000')
                             
    def _first_player_clicked(self) -> None:
        '''Command for when first player is done placing initial pieces'''
        self._first_player.destroy()

        self._second_player = tkinter.Button(
            master = self._play_window,
            text = (self._gamestate.switch_turn() + ' is ready'), font = DEFAULT_FONT,
            command = self._second_player_clicked)

        self._second_player.grid(
            row = 0, column = 0, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self._gamestate._turn = self._gamestate.switch_turn()

    def _second_player_clicked(self) -> None:
        '''Command for when second player is done placing initial pieces'''
        self._second_player.destroy()
        self._gamestate._turn = self._gamestate.switch_turn()
        self._canvas.unbind('<Button-1>')
        self._canvas.bind('<Button-1>', self._on_move_clicked)
        self._gamestate.score()
        self.score_board()

    def _on_move_clicked(self, event: tkinter.Event) -> None:
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        width_spacing = width / self._gamestate._columns
        height_spacing = height / self._gamestate._rows

        for row in range(self._gamestate._rows):
            if event.y in range(int(height_spacing*(row)), int(height_spacing*(row+1))):
                for col in range(self._gamestate._columns):
                    if event.x in range(int(width_spacing*(col)), int(width_spacing*(col+1))):
                        self._player_move = [row, col]                   
        self.play_game()
            
    def play_game(self) -> None:
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        width_spacing = width / self._gamestate._columns
        height_spacing = height / self._gamestate._rows
        invalid = False
        
        try:
            if self._gamestate.require_game_not_over() == True and invalid == False:
                self._gamestate.score()
                self.score_board()
            
            if self._gamestate.make_move(self._player_move) == True:
                invalid = False
                self._black_pieces.clear()
                self._white_pieces.clear()
                for row in range(self._gamestate._rows):
                    for col in range(self._gamestate._columns):
                        if self._gamestate._board[row][col] == 'B':
                            click_point = from_pixel((((col+1)*width_spacing)-(width_spacing/2)),
                            (((row+1)*height_spacing)-(height_spacing/2)), width, height)
                            self._black_pieces.all_spots().append(Spot(click_point, self._radiusx))
                        elif self._gamestate._board[row][col] == 'W':
                            click_point = from_pixel((((col+1)*width_spacing)-(width_spacing/2)),
                            (((row+1)*height_spacing)-(height_spacing/2)), width, height)
                            self._white_pieces.all_spots().append(Spot(click_point, self._radiusx))
                self._gamestate.score()
                self.score_board()
                self.redraw_board()
                if self._gamestate.require_game_not_over() == False:
                    self._gamestate._turn = self._gamestate.switch_turn()
                    self._gamestate.score()
                    self.score_board()
                    raise othello_game_logic.GameOverError
            self._gamestate.score()
            self.score_board()
            self.redraw_board()

        except othello_game_logic.InvalidMoveError:
            invalid = True
            
        except othello_game_logic.GameOverError:
            self._gamestate.score()
            self.score_board()
            self.winner()
            self._canvas.unbind('<Button-1>')
            
    def score_board(self) -> None:
        '''Displays the scoreboard which includes the turn'''
        self._score = tkinter.Label(
            master = self._play_window,
            text = "B: {}\t\tW: {}".format(self._gamestate._score[0], self._gamestate._score[1]),
            font = DEFAULT_FONT, background = 'white')
            
        self._score.grid(
            row = 0, column = 0, padx =10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self._show_turn = tkinter.Label(
            master = self._play_window,
            text = "{}'s Turn".format(self._gamestate._turn),
            font = DEFAULT_FONT, background = 'white')

        self._show_turn.grid(
            row = 2, column = 0, padx =10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
            
    def winner(self) -> None:
        '''Displays who the winner is'''
        winner = self._gamestate.winner()
        
        if winner == 'B':
            winner = 'Black'
        elif winner == 'W':
            winner = 'White'
        else:
            winner = 'Nobody'
            
        self._winner = tkinter.Label(
             master = self._play_window,
            text = "Game Over. {} Wins".format(winner),
            font = DEFAULT_FONT, background = 'white')

        self._winner.grid(
            row = 2, column = 0, padx =10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
                    
