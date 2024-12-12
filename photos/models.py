from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
class Album(models.Model):
    title = models.CharField(max_length=255)  # Nombre del álbum
    description = models.TextField(blank=True)  # Descripción opcional del álbum
    upload_date = models.DateTimeField(auto_now_add=True)  # Fecha de creación del álbum

    def __str__(self):
        return self.title

def album_upload_path(instance, filename):
    return f'album_{instance.album.id}/{filename}'

class Photo(models.Model):
    title = models.CharField(max_length=255)  # Título de la fotografía
    image = models.ImageField(upload_to=album_upload_path)  # Imagen de alta resolución
    reduced_image = models.ImageField(
        upload_to=album_upload_path, editable=False, null=True, blank=True
    )  # Imagen de baja resolución
    description = models.TextField(blank=True)  # Descripción opcional de la imagen
    upload_date = models.DateTimeField(auto_now_add=True, null=True)  # Fecha de subida automática
    likes = models.PositiveIntegerField(default=0)  # Número de likes
    album = models.ForeignKey(
        Album, related_name='photos', on_delete=models.CASCADE, null=True, blank=True
    )  # Relación con el álbum (opcional temporalmente)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Guarda la foto inicialmente
        super().save(*args, **kwargs)
        # Genera la imagen reducida
        if self.image and not self.reduced_image:
            img = Image.open(self.image)
            img.thumbnail((1100, 1100), Image.LANCZOS)  # Redimensionar a 800x800 píxeles

            # Guardar la imagen reducida en un archivo temporal
            img_io = BytesIO()
            img.save(img_io, format='JPEG', quality=80)
            img_content = ContentFile(img_io.getvalue(), name=f'reduced_{self.image.name}')

            # Asigna la imagen reducida al campo correspondiente
            self.reduced_image.save(img_content.name, img_content, save=False)

        # Guarda la instancia nuevamente para registrar la imagen reducida
        super().save(*args, **kwargs)