# Generated by Django 4.0.4 on 2022-05-23 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_move_training_pokemon_moves'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.pokemon')),
            ],
        ),
    ]
