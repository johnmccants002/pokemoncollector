from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('pokemons/', views.pokemons_index, name='index'),
    path('pokemons/<int:pokemon_id>', views.pokemons_detail, name = "detail"),
    path('pokemons/create/', views.PokemonCreate.as_view(), name='pokemons_create'),
    path('pokemons/<int:pk>/update', views.PokemonUpdate.as_view(), name="pokemons_update"),
    path('pokemons/<int:pk>/delete', views.PokemonDelete.as_view(), name="pokemons_delete"),
    path('pokemons/<int:pokemon_id>/add_training/', views.add_training, name='add_training'),
    path('pokemons/<int:pokemon_id>/assoc_move/<int:move_id>/', views.assoc_move, name='assoc_move'),
    path('pokemons/<int:pokemon_id>/add_photo', views.add_photo, name='add_photo'),
    path('accounts/signup/', views.signup, name='signup'),
]

urlpatterns += staticfiles_urlpatterns()