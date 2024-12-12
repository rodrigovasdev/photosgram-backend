# Generated by Django 4.2.16 on 2024-12-05 06:23

import datetime
from django.db import migrations, models
import django.db.models.deletion
import photos.models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RenameField(
            model_name='photo',
            old_name='titulo',
            new_name='title',
        ),
        migrations.AddField(
            model_name='photo',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='photo',
            name='upload_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 12, 5, 6, 23, 32, 727560, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='photo',
            name='imagen',
            field=models.ImageField(upload_to=photos.models.album_upload_path),
        ),
        migrations.AddField(
            model_name='photo',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='photos.album'),
        ),
    ]
