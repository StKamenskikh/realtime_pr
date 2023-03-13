import json
from asyncio import sleep
import asyncio
from grpc import aio
from datetime import datetime, timedelta
from random import randint

from channels.generic.websocket import AsyncWebsocketConsumer

from .DataProtocol import GRPCProto_pb2_grpc, GRPCProto_pb2


class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        for i in range(1000):
            await self.send(json.dumps({'message': randint(1, 100)}))
            await sleep(1)


class DataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        tags = self.scope['url_route']['kwargs']['tags'].split('_')[:-1]
        tagsId = []

        await asyncio.gather(*[self.AppendStream(tag) for tag in tags])

    async def AppendStream(self,tag):
        assetId = int(tag.split('g')[0][1:])
        tagId = []
        tagId.append(int(tag.split('t')[1]))

        arg = GRPCProto_pb2.ArgData(assetId=assetId,
                                    tagsId=tagId,
                                    timeStampFrom=1000)
        print(arg)
        async with aio.insecure_channel('localhost:6062') as channel:
            stub = GRPCProto_pb2_grpc.GRPCProtoStub(channel)
            async for response in stub.GetDataStream(arg):
                message = []
                for tagVal in response.tagsVal:
                    if tagVal.tagId == tagId[0]:
                        timeStamp = (timedelta(seconds=tagVal.timeStamp) + datetime(1970, 1, 1)).strftime(
                            '%m-%d-%Y %H:%M:%S')
                        message.append({'tagId': tagVal.tagId, 'DateTime': timeStamp,
                                        'value': tagVal.value, 'isGood': tagVal.isGood, 'tag': tag})
                await self.send(json.dumps(message))