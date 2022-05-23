from django.shortcuts import render, redirect
import os
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Pokemon, Training, Move, Photo
from .forms import TrainingForm
import uuid
import boto3
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def pokemons_index(request):
    pokemons = Pokemon.objects.filter(user=request.user)
    return render(request, 'pokemons/index.html', {'pokemons': pokemons})
@login_required
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

@login_required
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

@login_required
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

@login_required
def assoc_move(request, pokemon_id, move_id):
    Pokemon.objects.get(id=pokemon_id).moves.add(move_id)
    return redirect('detail', pokemon_id=pokemon_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


class PokemonCreate(LoginRequiredMixin, CreateView):
    model = Pokemon
    fields = ["name", "breed", "description", "age"]
    success_url = '/pokemons/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PokemonUpdate(LoginRequiredMixin, UpdateView):
    model = Pokemon
    fields = ["description"]
    success_url = '/pokemons/'

class PokemonDelete(LoginRequiredMixin, DeleteView):
    model = Pokemon
    success_url = '/pokemons/'

class MoveList(LoginRequiredMixin, ListView):
  model = Move

class MoveDetail(LoginRequiredMixin, DetailView):
  model = Move





