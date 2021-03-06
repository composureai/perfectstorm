# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-20 14:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import teacup.apiserver.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(unique=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ComponentLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='apiserver.Application')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(unique=True)),
                ('query', jsonfield.fields.JSONField(default=dict, validators=[teacup.apiserver.validators.validate_dict])),
                ('include', jsonfield.fields.JSONField(default=list, validators=[teacup.apiserver.validators.validate_list_of_strings])),
                ('exclude', jsonfield.fields.JSONField(default=list, validators=[teacup.apiserver.validators.validate_list_of_strings])),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.SlugField()),
                ('name', models.SlugField(unique=True)),
                ('content', models.TextField(default='')),
                ('options', jsonfield.fields.JSONField(default=dict)),
                ('params', jsonfield.fields.JSONField(default=dict)),
                ('add_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='apiserver.Group')),
                ('target_all_in', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='apiserver.Group')),
                ('target_any_of', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='apiserver.Group')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('protocol', models.CharField(choices=[('tcp', 'TCP'), ('udp', 'UDP')], max_length=8)),
                ('port', models.PositiveIntegerField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='apiserver.Group')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('name', models.SlugField()),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('running', 'Running'), ('done', 'Done'), ('error', 'Error')], default='pending', max_length=16)),
                ('arguments', jsonfield.fields.JSONField(default=dict)),
                ('result', jsonfield.fields.JSONField(default=dict)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('heartbeat', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.AddField(
            model_name='componentlink',
            name='from_component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apiserver.Group'),
        ),
        migrations.AddField(
            model_name='componentlink',
            name='to_service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apiserver.Service'),
        ),
        migrations.AddField(
            model_name='application',
            name='components',
            field=models.ManyToManyField(to='apiserver.Group'),
        ),
        migrations.AddField(
            model_name='application',
            name='expose',
            field=models.ManyToManyField(to='apiserver.Service'),
        ),
        migrations.AlterUniqueTogether(
            name='service',
            unique_together=set([('name', 'group')]),
        ),
        migrations.AlterUniqueTogether(
            name='componentlink',
            unique_together=set([('application', 'from_component', 'to_service')]),
        ),
    ]
