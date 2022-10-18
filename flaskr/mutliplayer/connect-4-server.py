from concurrent import futures
import logging
import math
import time
from typing import AsyncIterable

from grpc import aio
import asyncio
import grpc
import connect_4_pb2
import connect_4_pb2_grpc
# import connect_4_resources

interim_move = -1

R = 1
Y = 2
DRAW = 3

# player_1_move
# player_2_move

class JoinReq:
    roomid = 0
    clientid = []

class Connect4Servicer(connect_4_pb2_grpc.Connect_4Servicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self):
        self.room = {"id": 43, "members": []}
        pass

    async def JoinRoom(self, request, context) -> AsyncIterable[connect_4_pb2.JoinResponse]:
        global player_1_id
        global player_2_id
        print(self.room)
        if not request.id in self.room['members']:
            if len(self.room['members']) < 1:
                player_1_id = request.id
                self.room['members'].append({'id': request.id, 'colour': request.colour})
                JoinRequest = connect_4_pb2.JoinResponse(roomid=str(self.room['id']), clientid=str(self.room['members']), colour=request.colour)
            else:
                player_2_id = request.id
                for m in self.room['members']:
                    if m['colour'] == R: new_colour = Y
                    else: new_colour = R
                self.room['members'].append({'id': request.id, 'colour': new_colour})
                JoinRequest = connect_4_pb2.JoinResponse(roomid=str(self.room['id']), clientid=str(self.room['members']), colour=new_colour)
            print(self.room)
            yield JoinRequest

    def End(self, request, context):
        print('End game')
        global interim_move
        interim_move = request.column
        return connect_4_pb2.EndResponse(complete=True)

    async def Move(self, request, context):
        print('Move')
        global interim_move
        interim_move = request.column
        await asyncio.sleep(1)
        interim_move = -1

        while interim_move == -1:
            await asyncio.sleep(1)
        return connect_4_pb2.MoveResponse(column=interim_move)

    async def FirstMoveP2(self, request, context):
        print('First move p2')
        global interim_move
        while interim_move == -1:
            await asyncio.sleep(1)
        return connect_4_pb2.MoveResponse(column=interim_move)


async def serve():
    server = aio.server(futures.ThreadPoolExecutor(max_workers=10))
    connect_4_pb2_grpc.add_Connect_4Servicer_to_server(
        Connect4Servicer(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(serve())