# Generated by Django 2.2.17 on 2021-01-15 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Requisites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pre_req', models.CharField(blank=True, default='N/A', max_length=100)),
                ('Co_req', models.CharField(blank=True, default='N/A', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=7)),
                ('department', models.CharField(choices=[('CSM', 'Camborne School of Mines'), ('Comp', 'Computing'), ('Eng', 'Engineering'), ('Maths', 'Mathematics'), ('NatSci', 'Natural Sciences'), ('Phy', 'Physics'), ('Bio', 'Biosciences'), ('Geo', 'Geography'), ('Other', 'Other')], max_length=200)),
                ('category', models.CharField(blank=True, default='na', max_length=200)),
                ('sub_category', models.CharField(blank=True, default='na', max_length=200)),
                ('year', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('1,2', '1,2'), ('na', 'N/A')], max_length=20)),
                ('term', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('12', '1 and 2'), ('1,2,3', '1,2,3'), ('1 or 2', '1 or 2'), ('1 or 3', '1 or 3'), ('2 or 3', '2 or 3'), ('Other', 'Other')], max_length=20)),
                ('credits', models.IntegerField(default=15)),
                ('lecturer', models.CharField(blank=True, max_length=150)),
                ('core_Natural_Sciences', models.CharField(blank=True, max_length=1)),
                ('core_Mathematics', models.CharField(blank=True, max_length=1)),
                ('core_Physics', models.CharField(blank=True, max_length=1)),
                ('core_Biological_Sciences', models.CharField(blank=True, max_length=1)),
                ('core_Biochemistry', models.CharField(blank=True, max_length=1)),
                ('core_Biological_and_Medicinal_Chemistry', models.CharField(blank=True, max_length=1)),
                ('core_Physics_MPhys', models.CharField(blank=True, max_length=1)),
                ('Natural_Sciences_History', models.CharField(blank=True, max_length=1)),
                ('Topic_Pathway', models.CharField(blank=True, default='N/A', max_length=100)),
                ('module_descriptor', models.URLField(max_length=500)),
                ('requisites', models.ManyToManyField(blank=True, to='department.Requisites')),
            ],
        ),
    ]