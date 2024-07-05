# Generated by Django 5.0.6 on 2024-07-05 15:51

import core.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('icon', models.ImageField(blank=True, upload_to='games/<django.db.models.fields.CharField>')),
            ],
        ),
        migrations.CreateModel(
            name='Gamer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=core.models.user_directory_path)),
                ('games', models.ManyToManyField(blank=True, to='core.game')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Collision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accept', models.BooleanField()),
                ('match', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coll_fr_user', to=settings.AUTH_USER_MODEL)),
                ('viewed_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coll_fr_viewed_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'viewed_user')},
            },
        ),
    ]