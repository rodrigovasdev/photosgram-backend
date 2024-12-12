from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Photo, Album
from .forms import PhotoForm, AlbumForm
# Create your views here.
def photosJson(request):
    fotografias = Photo.objects.all()  # Obtener todas las imágenes
    if not fotografias:
        return JsonResponse({'mensaje': 'No hay imágenes disponibles'}, status=404)

    urls = [f"https://{fotografia.image.storage.bucket_name}.s3.{fotografia.image.storage.region_name}.amazonaws.com/{fotografia.image.name}" for fotografia in fotografias]
    return JsonResponse({'urls': urls})

def newPhotoView(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/photos')  # Redirige a la vista que lista todas las imágenes (puede ser la vista JSON)
    else:
        form = PhotoForm()
    return render(request, 'new_photo.html', {'form': form})



def newAlbumView(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/photos')  # Redirige a la vista que lista todas las imágenes (puede ser la vista JSON)
    else:
        form = AlbumForm()
    return render(request, 'new_album.html', {'form': form})


def albumView(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    fotos = album.photos.all()
    fotos_data = [
        {
            'id': foto.id,
            'title': foto.title,
            'description': foto.description,
            'upload_date': foto.upload_date,
            'likes': foto.likes,
            'image_url': request.build_absolute_uri(foto.image.url),
            'reduced_image_url': request.build_absolute_uri(foto.reduced_image.url) if foto.reduced_image else None 
        }
        for foto in fotos
    ]
    return JsonResponse({'album': album.title,'album_description': album.description , 'images': fotos_data})

# Vista para traer todos los álbumes
def allAlbumsView(request):
    albums = Album.objects.all()
    albums_data = [
        {
            'id': album.id,
            'name': album.title,
            'description': album.description,
            'creation_date': album.upload_date,
            'cover_url': 'https://photosgrambucket.s3.us-east-2.amazonaws.com/'+album.photos.first().reduced_image.name.split('?')[0]
            if album.photos.exists() and album.photos.first().reduced_image else None
        }
        for album in albums
    ]
    return JsonResponse({'albums': albums_data})

# Vista para traer los detalles de una photo por ID
#BORRAR TODOS LOS REGISTROS y Poblar para comprobar la cover reduced.
def photoView(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    album = photo.album

    # Obtener la foto anterior dentro del mismo álbum (si existe)
    previous_photo = None
    if album:
        previous_photo = Photo.objects.filter(album=album, id__lt=photo.id).order_by('-id').first()

    # Obtener la foto siguiente dentro del mismo álbum (si existe)
    next_photo = None
    if album:
        next_photo = Photo.objects.filter(album=album, id__gt=photo.id).order_by('id').first()

    photo_data = {
        'id': photo.id,
        'title': photo.title,
        'description': photo.description,
        'upload_date': photo.upload_date,
        'likes': photo.likes,
        'image_url': 'https://photosgrambucket.s3.us-east-2.amazonaws.com/' + photo.image.name.split('?')[0],
        'album_id': album.id if album else None,
        'album_name': album.title if album else None,
        'previous_photo_id': previous_photo.id if previous_photo else None,
        'next_photo_id': next_photo.id if next_photo else None
    }

    return JsonResponse({'photo': photo_data})

