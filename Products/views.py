from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from Auth.models import UserProfile
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from Products.models import Produk, GambarProduk, Kategori
from asgiref.sync import async_to_sync, sync_to_async
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from sawarung.consumer import ProductConsumer
import asyncio
# Create your views here.


async def add_data_async(token, data):
    print('IM INSIDE THISSSSSSSSSSSSSSSSSS .............................')
    channel_layer = get_channel_layer()

    await channel_layer.group_send(
            'product',
            {
                "type": "product_new_local",
                "product_data": data,
            },
        )
    print('SKIIPPPPPPPPPPPPPPP...............................')
@csrf_exempt
def getProductsByUser(request):
    try:
        data = json.loads(request.body)
        token = data['token']
        curr_token = Token.objects.get(key=token)
        if not curr_token:
            return JsonResponse({'message':'Maaf autorisasi gagal' ,'status':401})
        user = curr_token.user
        products = Produk.objects.select_related('pemilik__userprofile').prefetch_related('review_produk__pemilik__userprofile').all()
        products_list = []
        for product in products:
            products_list.append(product.to_dict_after_select_profile())
        return JsonResponse({'message': 'berhasil load produk', 'products': products_list, 'status': 200})
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'Terdapat kesalahan internal pada server', 'status':500})


@csrf_exempt
def create_product(request):
    try:
        data = json.loads(request.body)
        token = data['token']
        print(token)
        print(data['kategori'])
        curr_token = Token.objects.get(key=token)
        if not curr_token:
            return JsonResponse({'message':'Maaf autorisasi gagal' ,'status':401})
        
        print('HEAL THE WORLD -----------------------------------------------------')
        user = curr_token.user
        new_product = Produk(pemilik=user, nama= data['nama'], id_produk= data['productId'],
                 for_sale = data['for_sale'], harga=data['harga'], stok= data['stok'],
                 deskripsi = data['deskripsi'])
        new_product.save()

        gambar_list = data['gambar']
        images = []
        categories_str = data['kategori']
        categories = []
        print('I AM CONFUSED -----------------------------------------------------')
        for imageUrl in gambar_list:
            image = GambarProduk.objects.create(gambar=imageUrl)
            images.append(image)
        for category_str in categories_str:
            category, created = Kategori.objects.get_or_create(nama=category_str)
            categories.append(category)
        print('MY LIFE STRESSED -----------------------------------------------------')
        new_product.gambar_produk.add(*images)
        new_product.kategori.add(*categories)
        print('ITS GOING TO BE CRAZY -----------------------------------------------------')
        selected_product = Produk.objects.select_related('pemilik__userprofile').get(id_produk=data['productId'])
       
        # Kirim pesan ke grup "product_updates"
        
        print('apa sih..............................................')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        async_result = loop.run_until_complete(add_data_async(token=token, data=selected_product.to_dict_after_select_profile()))
        loop.close()
        
        return  JsonResponse({'message': 'berhasil menambahkan produk', 
                                'status':200})             
    except Exception as e:
        print(e)
        return  JsonResponse({'message': 'Gagal menambahkan produk', 'productId': data['productId'],
                             'status':500})  