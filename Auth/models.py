from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    username = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True )
    nama_lengkap = models.CharField(max_length=250)
    email = models.EmailField(max_length=254 )
    password = models.TextField()
    alamat = models.TextField(null=True, blank=True)
    nomor_telepon = models.CharField(max_length=15, null=True, blank=True)
    gambar_profil = models.TextField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.user.username
    def to_dict(self):
        created_at_str = self.date_joined.strftime('%Y-%m-%dT%H:%M:%S')
        return {
            'id': self.user.id,
            'username': self.username,
            'description': self.description,
            'nama_lengkap': self.nama_lengkap,
            'email': self.email,
            'alamat': self.alamat,
            'nomor_telepon': self.nomor_telepon,
            'gambar_profil': self.gambar_profil,
            'date_joined': created_at_str
        }
