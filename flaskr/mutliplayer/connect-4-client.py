from __future__ import print_function
from concurrent.futures import ThreadPoolExecutor

import logging
from pydoc import cli
import random
import threading
from typing import Iterator
from urllib import response

import tkinter as tk
import grpc
from grpc import aio
import asyncio
import connect_4_pb2
import connect_4_pb2_grpc
from backend import game
import nest_asyncio
# import connect_4_resources

R = 1
Y = 2
DRAW = 3

stub = ""
client_colour = R

class Connect4_Client:
    def __init__(self, executor: ThreadPoolExecutor, channel: grpc.Channel,
                 id: int) -> None:
        self._executor = executor
        self._channel = channel
        self._id = id
        self._stub = connect_4_pb2_grpc.Connect_4Stub(self._channel)
        self._connected_to_room = threading.Event()
        self._consumer_future = None

    def _response_watcher(self, response_iterator: connect_4_pb2.JoinResponse):
        print('Here')
        # print(response_iterator.count)
        print()
        received_response = False
        while not received_response:
            for response in response_iterator:
                received_response = True
                print(response)
                print(response.roomid)
                self._connected_to_room.set()
        print('Here 2')

    def await_server_response(self):
        print('Attempting to join server')
        self._connected_to_room.wait(timeout=None)
        if self._consumer_future.done():
            self._consumer_future.result()
        return True

async def guide_first_P2(stub: connect_4_pb2_grpc.Connect_4Stub, id, colour, col):
    global client_colour
    r = await stub.FirstMoveP2(connect_4_pb2.InitRequest(id=str(my_id)), timeout=6000)
    print(f'opposition move {r.column}')
    if client_colour == R: opp_colour = Y
    else: opp_colour = R
    local_game.make_move(r.column, opp_colour,local_game.board)
    local_game.update_player()
    c.draw_grid()

async def guide_move(stub: connect_4_pb2_grpc.Connect_4Stub, id, colour, col):
    global client_colour
    print('Moving to column ' + str(col))
    if not local_game.in_progress:
        r = stub.End(connect_4_pb2.MoveRequest(column=col))
        print('You win! (or there\'s a draw)')
    else:
        r = await stub.Move(connect_4_pb2.MoveRequest(column=col))
    print(f'opposition move {r.column}')
    if client_colour == R: opp_colour = Y
    else: opp_colour = R
    local_game.make_move(r.column, opp_colour,local_game.board)
    if not local_game.in_progress:
        #game has ended
        print('You lose (or there is a draw)')
        pass
    local_game.curr_player = client_colour
    c.draw_grid()

async def guide_join_request(stub: connect_4_pb2_grpc.Connect_4Stub, id, colour):
    global client_colour
    print(f"My id is {id}")

    response = stub.JoinRoom(connect_4_pb2.JoinRequest(id=str(id), colour=colour), timeout=6000)
    async for r in response:
        print(r.roomid)
        print(r.clientid)
        client_colour = r.colour
        # print(responses)
        
        # self._stub.

        # for response in responses:
            # print(f"Joined room {response.roomid} with {response.clientid}")


async def run() -> None:
    global client_colour
    global stub
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    client_colour = local_game.curr_player
    async with aio.insecure_channel('localhost:50051') as channel:
        stub = connect_4_pb2_grpc.Connect_4Stub(channel)
        print("-------------- RouteChat --------------")
        await guide_join_request(stub, my_id, client_colour)
        print(client_colour)
        tk.Canvas.create_circle = _create_circle
        tk.Canvas.draw_grid = _draw_grid
        root.resizable(width=False, height=False)

        c.pack(fill=tk.BOTH, expand=True)
        highlighted_col = 0

        c.bind("<Key>", key)
        c.bind("<Button-1>", callback)
        c.bind('<Motion>', motion)
        c.bind('<Configure>', create_grid)

        c.draw_grid()
        if client_colour == Y:
            await guide_first_P2(stub, my_id, client_colour, 0)
        root.mainloop()
    #player 2

    # for r in response:
    #     print(r.roomid)
    #     print(r.clientid)





def create_grid(event=None):
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

def _draw_grid(self, highlight_cell=None):
    print(highlight_cell)
    board = local_game.board
    curr_player = local_game.curr_player
    c.delete("counter")
    if highlight_cell != None and local_game.in_progress:
        highlight_x = highlight_cell
        highlight_y = local_game.find_lowest_row(highlight_cell, board)
    for x in range(7):
        for y in range(6):
            fill = 'MidnightBlue'
            if highlight_cell != None and local_game.in_progress:
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

async def callback(event):
    global client_colour
    global stub
    if local_game.in_progress and client_colour == local_game.curr_player:
        col = max(0, min(event.x//100, 6))
        local_game.make_move(col, local_game.curr_player, local_game.board)
        
        local_game.update_player()

        c.draw_grid()
        asyncio.get_event_loop().run_until_complete(update_move(col))
        # asyncio.run(update_move(col))

async def update_move(col):
    await guide_move(stub, my_id, client_colour, col)

def motion(event):
    col = max(0, min(event.x//100, 6))
    global highlighted_col
    global client_colour
    if col != highlighted_col and client_colour == local_game.curr_player:
        highlighted_col = col
        c.draw_grid(col)

# def start_loop():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.create_task(updateLoans())
#     loop.run_forever()

nest_asyncio.apply()
my_id = random.randint(0,100)
local_game = game()
root = tk.Tk(screenName="Connect 4")
c = tk.Canvas(root, height=600, width=700, bg='blue')
highlighted_col = 0
if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())