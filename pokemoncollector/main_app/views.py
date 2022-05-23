from django.shortcuts import render, redirect
import os
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Pokemon, Training, Move, Photo
from .forms import TrainingForm
import uuid
import boto3


# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def pokemons_index(request):
    pokemons = Pokemon.objects.all()
    return render(request, 'pokemons/index.html', {'pokemons': pokemons})

def pokemons_detail(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
  # Get the toys the cat doesn't have
    moves_pokemon_doesnt_have = Move.objects.exclude(id__in = pokemon.moves.all().values_list('id'))
    training_form = TrainingForm()
    return render(request, 'pokemons/detail.html', {
    'pokemon': pokemon, 'training_form': training_form,
    # Add the toys to be displayed
    'moves': moves_pokemon_doesnt_have
  })

def add_training(request, pokemon_id):
      # create a ModelForm instance using the data in request.POST
    form = TrainingForm(request.POST)
   # validate the form
    if form.is_valid():
    # don't save the form to the db until it
    # has the cat_id assigned
      new_training = form.save(commit=False)
      new_training.pokemon_id = pokemon_id
      new_training.save()
    return redirect('detail', pokemon_id=pokemon_id)

def add_photo(request, pokemon_id):
  print('In the add photo function')
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, pokemon_id=pokemon_id)
    except:
      print('An error occurred while uploading to s3')
  return redirect("detail", pokemon_id=pokemon_id)

def assoc_move(request, pokemon_id, move_id):
    Pokemon.objects.get(id=pokemon_id).moves.add(move_id)
    return redirect('detail', pokemon_id=pokemon_id)


class PokemonCreate(CreateView):
    model = Pokemon
    fields = ["name", "breed", "description", "age"]
    success_url = '/pokemons/'

class PokemonUpdate(UpdateView):
    model = Pokemon
    fields = ["description"]
    success_url = '/pokemons/'

class PokemonDelete(DeleteView):
    model = Pokemon
    success_url = '/pokemons/'

class MoveList(ListView):
  model = Move

class MoveDetail(DetailView):
  model = Move





