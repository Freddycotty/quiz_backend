# Generated by Django 3.2.13 on 2022-05-06 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0026_alter_preguntas_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='preguntas',
            old_name='photo',
            new_name='imagen',
        ),
    ]
