# Generated by Django 3.1.3 on 2020-12-16 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagram', '0002_auto_20201216_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='core',
            field=models.BooleanField(default=False),
        ),
    ]
