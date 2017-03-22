# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 22:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Secret',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            managers=[
                ('secretManager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=255)),
            ],
            managers=[
                ('userManager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='secret',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created', to='new_app.User'),
        ),
        migrations.AddField(
            model_name='secret',
            name='users',
            field=models.ManyToManyField(related_name='secrets', to='new_app.User'),
        ),
    ]