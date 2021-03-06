# Generated by Django 3.2.13 on 2022-05-05 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0018_auto_20220505_1716'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='preguntas',
            options={'ordering': ['posicion'], 'verbose_name': 'pregunta', 'verbose_name_plural': 'preguntas'},
        ),
        migrations.AlterField(
            model_name='respuestas',
            name='pregunta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='respuesta_pregunta', to='quiz.preguntas'),
        ),
    ]
