# Generated by Django 4.2.19 on 2025-03-03 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_word_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='web.uploadedfile'),
        ),
    ]
