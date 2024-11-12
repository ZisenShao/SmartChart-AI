# Generated by Django 5.1.2 on 2024-10-14 20:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('my_chart_id', models.CharField(max_length=255, null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionLog',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('question_text', models.TextField()),
                ('answer_text', models.TextField()),
                ('date_asked', models.DateTimeField(auto_now_add=True)),
                ('confidence_score', models.FloatField()),
                ('source', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalData',
            fields=[
                ('medical_data_id', models.AutoField(primary_key=True, serialize=False)),
                ('data_type', models.CharField(max_length=255)),
                ('data_content', models.JSONField()),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
                ('source', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
        ),
        migrations.CreateModel(
            name='ChatSession',
            fields=[
                ('session_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_started', models.DateTimeField(auto_now_add=True)),
                ('date_ended', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('message_id', models.AutoField(primary_key=True, serialize=False)),
                ('message_text', models.TextField()),
                ('message_type', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.chatsession')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
        ),
    ]
