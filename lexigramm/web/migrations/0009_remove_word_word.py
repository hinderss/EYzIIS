# Generated by Django 4.2.19 on 2025-03-03 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_word_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='word',
        ),
    ]
