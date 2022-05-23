from django.contrib import admin
from .models import Photo, Pokemon, Training, Move, Move

admin.site.register(Pokemon)
admin.site.register(Training)
admin.site.register(Move)
admin.site.register(Photo)

# Register your models here.
