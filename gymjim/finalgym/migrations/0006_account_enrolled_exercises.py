# Generated by Django 4.2.1 on 2023-06-02 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalgym', '0005_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='enrolled_exercises',
            field=models.ManyToManyField(related_name='enrolled_users', to='finalgym.exercise'),
        ),
    ]
