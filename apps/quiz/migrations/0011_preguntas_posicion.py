# Generated by Django 3.2.13 on 2022-05-05 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_alter_respuestas_pregunta'),
    ]

    operations = [
        migrations.AddField(
            model_name='preguntas',
            name='posicion',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
