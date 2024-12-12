from django import forms
from .models import Photo, Album

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = '__all__'
        exclude = ['likes']

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = '__all__'
