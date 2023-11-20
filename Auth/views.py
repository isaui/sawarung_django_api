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
import json
# Create your views here.
@csrf_exempt
@require_http_methods(["OPTIONS", "POST"])
def register(request):
    print('HELLO WORLD----------------------------------------')
    if request.method == "POST":
        data = json.loads(request.body) 
        username= data['username']
        email = data['email']
        fullname = data['fullname']
        password1 = data['password1']
        password2 = data['password2']
        profile_picture = data['photo_profile']
        if password1 != password2:
            return JsonResponse({'message': 'Password yang dimasukkan tidak sama', 'status':401})
        if ' ' in username:
            return JsonResponse({'message': 'Username tidak boleh kosong atau  mengandung spasi', 'status': 400})
        if ' ' in email:
            return JsonResponse({'message': 'Email tidak boleh kosong atau  mengandung spasi', 'status': 400})
        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            return JsonResponse({'message': 'Username atau email sudah dipakai pengguna lain', 'status': 409})
        try:
            user = User.objects.create_user(username, email=email, password=password1)
            user.save()
            userProfile = UserProfile(user=user, username=username,gambar_profil=profile_picture, nama_lengkap=fullname, password=password1, email=email)
            userProfile.save()
            return JsonResponse({'message': 'Berhasil membuat akun', 'status': 201})
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Terdapat kesalahan internal', 'status': 500})

@csrf_exempt
@require_http_methods(["OPTIONS", "POST"])     
def loginUser(request):
    print('HELLOWORLD2----------------------------------------------')
    if request.method == 'POST':
        data = json.loads(request.body)
        username= data['username']   
        password = data['password']
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return JsonResponse({'message': 'Login berhasil', 'token': token.key, 'status': 200})
            return  JsonResponse({'message': 'Username atau password salah', 'status': 401})
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Metode permintaan tidak valid', 'status': 400})
        
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def logout_user(request):
    try:
       data = json.loads(request.body) 
       token = data['token']
       print(token)
       curr_token = Token.objects.get(key=token)
       curr_token.delete()
       return JsonResponse({'message':'Berhasil logout', 'status':200})
    except Exception as e:
        print(e)
        return JsonResponse({'message':'Gagal logout', 'status':500})

@csrf_exempt
def get_user_data(request):
    try:
        data = json.loads(request.body)
        token = data['token']
        curr_token = Token.objects.get(key=token)
        if not curr_token:
            return JsonResponse({'message':'Gagal mengirim data' ,'status':401})
        user = curr_token.user
        profile = UserProfile.objects.get(user=user)
        return JsonResponse({'message': 'Berhasil mengirim data', 'user_profile':profile.to_dict(),'status': 200})
    except Token.DoesNotExist:
         return JsonResponse({'message': 'Token tidak valid','status': 401})
    except Exception as e:
        print(e)
        return JsonResponse({'message': 'Terjadi kesalahan dalam server', 'status': 500})
    