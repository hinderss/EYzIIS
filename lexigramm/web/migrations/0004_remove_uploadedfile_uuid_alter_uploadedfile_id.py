# Generated by Django 4.2.19 on 2025-03-02 19:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_uploadedfile_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadedfile',
            name='uuid',
        ),
        migrations.AlterField(
            model_name='uploadedfile',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
