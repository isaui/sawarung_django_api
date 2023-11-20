from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Kategori(models.Model):
    nama = models.CharField(max_length=50)

    def __str__(self):
        return self.nama

class GambarProduk(models.Model):
    gambar = models.TextField()

    def __str__(self):
        return str(self.gambar)
    
class ReviewProduk(models.Model):
    pemilik = models.ForeignKey(User, on_delete=models.CASCADE)
    gambar_review = models.ManyToManyField(GambarProduk, related_name="gambar_review")
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    def to_dict_after_get_profile(self):
        created_at_str = self.created_at.strftime('%Y-%m-%dT%H:%M:%S')
        return {
            'pemilik': self.pemilik.userprofile.to_dict(),
            'review': {
                'text': self.text,
                'created_at': created_at_str,
                'gambar':  [foto.gambar for foto in self.gambar_review.all()]
            }
        }


class Produk(models.Model):
    pemilik = models.ForeignKey(User, on_delete=models.CASCADE)
    id_produk = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField()
    harga = models.DecimalField(max_digits=16, decimal_places=2)
    stok = models.PositiveIntegerField()
    for_sale = models.BooleanField(default=False)
    kategori = models.ManyToManyField(Kategori, related_name="kategori_produk")  # Many-to-Many ke Kategori
    gambar_produk = models.ManyToManyField(GambarProduk, related_name="gambar_produk")
      # Many-to-Many ke GambarProduk
    created_at = models.DateTimeField(default=timezone.now)
    review_produk = models.ManyToManyField(ReviewProduk)

    def to_dict(self):
        return {
            'id_produk':self.id_produk,
            'nama':self.nama,
            'dijual': self.for_sale,
            'deskripsi': self.deskripsi,
            'harga': self.harga,
            'stok':self.stok,
            'kategori':[kategori.nama for kategori in self.kategori.all()],
            'gambar':[foto.gambar for foto in self.gambar_produk.all()],
            'created_at':self.created_at
        }
    
    def to_dict_after_select_profile(self):
        created_at_str = self.created_at.strftime('%Y-%m-%dT%H:%M:%S')
        return {
            'pemilik': self.pemilik.userprofile.to_dict(),
            'product': {
                'id_produk':str(self.id_produk),
                'nama':self.nama,
                'dijual': self.for_sale,
                'deskripsi': self.deskripsi,
                'harga': str(self.harga),
                'stok':str(self.stok),
                'kategori':[kategori.nama for kategori in self.kategori.all()],
                'gambar':[foto.gambar for foto in self.gambar_produk.all()],
                'created_at': created_at_str
            },
            'review_produk':[review.to_dict_after_get_profile() for review in self.review_produk.all()]
        }
    def __str__(self):
        return self.nama
