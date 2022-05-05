# Generated by Django 3.2.13 on 2022-05-05 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_preguntas_nombre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Respuestas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detalle', models.CharField(max_length=250)),
                ('verdadero', models.BooleanField()),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respuesta_pregunta', to='quiz.quiz')),
            ],
            options={
                'verbose_name': 'respuesta',
                'verbose_name_plural': 'respuestas',
                'db_table': 'respuestas',
                'ordering': ['-id'],
            },
        ),
    ]
