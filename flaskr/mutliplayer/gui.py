from backend import game
import tkinter as tk

R = 1
Y = 2

class connect4board:
    def create_grid(c, event=None):
        w = c.winfo_width() # Get current width of canvas
        h = c.winfo_height() # Get current height of canvas
        c.delete('grid_line') # Will only remove the grid_line

        # Creates all vertical lines at intevals of 100
        for i in range(0, w, 100):
            c.create_line([(i, 0), (i, h)], tag='grid_line', width=3)

        # Creates all horizontal lines at intevals of 100
        for i in range(0, h, 100):
            c.create_line([(0, i), (w, i)], tag='grid_line', width=3)

    def _create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def _draw_grid(c, self, curr_game, highlight_cell=None):
        board = curr_game.board
        curr_player = curr_game.curr_player
        c.delete("counter")
        if highlight_cell != None and curr_game.in_progress:
            highlight_x = highlight_cell
            highlight_y = curr_game.find_lowest_row(highlight_cell, board)
        for x in range(7):
            for y in range(6):
                fill = 'MidnightBlue'
                if highlight_cell != None and curr_game.in_progress:
                    if x == highlight_x and y == highlight_y:
                        if curr_player == R:
                            fill = 'IndianRed1'
                        elif curr_player == Y:
                            fill = 'khaki1'
                if board[y][x] == R:
                    fill = 'red'
                elif board[y][x] == Y:
                    fill = 'yellow'
                c.create_circle(x*100 + 50, y*100 + 50, 40, fill=fill, width=0, tag='counter')

    def key(event):
        print("pressed", repr(event.char))

    def callback(event):
        if new_game.in_progress:
            col = max(0, min(event.x//100, 6))
            new_game.make_move(col, new_game.curr_player, new_game.board)
            new_game.update_player()
            c.draw_grid(new_game)

    def motion(event):
        col = max(0, min(event.x//100, 6))
        global highlighted_col
        if col != highlighted_col:
            highlighted_col = col
            c.draw_grid(new_game, col)

    new_game = game()
    tk.Canvas.create_circle = _create_circle
    tk.Canvas.draw_grid = _draw_grid


    root = tk.Tk(screenName="Connect 4")
    root.resizable(width=False, height=False)

    c = tk.Canvas(root, height=600, width=700, bg='blue')
    c.pack(fill=tk.BOTH, expand=True)
    highlighted_col = 0

    c.bind("<Key>", key)
    c.bind("<Button-1>", callback)
    c.bind('<Motion>', motion)
    c.bind('<Configure>', create_grid)

    c.draw_grid(new_game)
    root.mainloop()