# Generated by Django 5.1 on 2024-08-23 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0002_evolutionline'),
    ]

    operations = [
        migrations.AddField(
            model_name='evolutionline',
            name='sprites',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
