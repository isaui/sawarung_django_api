# Generated by Django 4.2.7 on 2023-11-20 03:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Products', '0002_produk_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewProduk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('gambar_review', models.ManyToManyField(related_name='gambar_review', to='Products.gambarproduk')),
                ('pemilik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='produk',
            name='review_produk',
            field=models.ManyToManyField(to='Products.reviewproduk'),
        ),
    ]
