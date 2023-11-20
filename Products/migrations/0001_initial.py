# Generated by Django 4.2.7 on 2023-11-10 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GambarProduk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gambar', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Kategori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Produk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_produk', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('nama', models.CharField(max_length=100)),
                ('deskripsi', models.TextField()),
                ('harga', models.DecimalField(decimal_places=2, max_digits=16)),
                ('stok', models.PositiveIntegerField()),
                ('for_sale', models.BooleanField(default=False)),
                ('gambar_produk', models.ManyToManyField(related_name='gambar_produk', to='Products.gambarproduk')),
                ('kategori', models.ManyToManyField(related_name='kategori_produk', to='Products.kategori')),
                ('pemilik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
