# Generated by Django 3.1.3 on 2020-12-16 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagram', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='sub_category',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='module',
            name='department',
            field=models.CharField(choices=[('CSM', 'Camborne School of Mines'), ('Comp', 'Computing'), ('Eng', 'Engineering'), ('Maths', 'Mathematics'), ('NatSci', 'Natural Sciences'), ('Phy', 'Physics and Astronomy'), ('Bio', 'Biosciences')], max_length=200),
        ),
    ]
