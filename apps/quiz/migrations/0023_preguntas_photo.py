# Generated by Django 3.2.13 on 2022-05-06 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0022_auto_20220506_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='preguntas',
            name='photo',
            field=models.ImageField(blank=True, upload_to='static'),
        ),
    ]
