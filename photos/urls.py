from django.urls import path
from .views import photosJson, newPhotoView, newAlbumView, albumView, allAlbumsView,photoView

urlpatterns = [
    path('',photosJson,name='photos'),
    path('photo/new',newPhotoView,name='newphotos'),
    path('album/new',newAlbumView,name='newphotos'),
    path('album/<int:album_id>',albumView,name='album'),
    path('album/all',allAlbumsView,name='allalbum'),
    path('photo/<int:photo_id>',photoView,name='photoView'),
]
