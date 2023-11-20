import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
class ProductConsumer(AsyncWebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.token = None

    async def connect(self):
        
        await self.accept()
        self.token = self.scope['url_route']['kwargs']['token']
        try:
          await   self.channel_layer.group_add(
            'product',
            self.channel_name,
        )
        except Exception as e:
            print(e)

    async def disconnect(self, close_code):
         await self.channel_layer.group_discard(
            'product',
            self.channel_name,
        )
    async def product_new_local(self, event):
        print('MARI KITA COBA MENUSUK................ >')
        product_data = event['product_data']
        print('ITS HORRIBLE >>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        # Kirim data produk ke client melalui WebSocket
        await self.send(json.dumps({
            'type': 'product',
            'product_data': product_data,
        }))
        print('berhasil mengirim data!!!----------------------------------------')
        