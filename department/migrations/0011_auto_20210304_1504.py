# Generated by Django 3.1.7 on 2021-03-04 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0010_auto_20210122_1550'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='Co_req',
        ),
        migrations.RemoveField(
            model_name='module',
            name='Pre_req',
        ),
        migrations.RemoveField(
            model_name='module',
            name='category',
        ),
        migrations.RemoveField(
            model_name='module',
            name='code',
        ),
        migrations.RemoveField(
            model_name='module',
            name='core_Biochemistry',
        ),
        migrations.RemoveField(
            model_name='module',
            name='core_Biological_Sciences',
        ),
        migrations.RemoveField(
            model_name='module',
            name='core_Biological_and_Medicinal_Chemistry',
        ),
        migrations.RemoveField(
            model_name='module',
            name='core_Mathematics',
        ),
        migrations.RemoveField(
            model_name='module',
            name='core_Natural_Sciences',
        ),
        migrations.RemoveField(
            model_name='module',
            name='core_Physics_BPhys',
        ),
        migrations.RemoveField(
            model_name='module',
            name='core_Physics_MPhys',
        ),
        migrations.RemoveField(
            model_name='module',
            name='credits',
        ),
        migrations.RemoveField(
            model_name='module',
            name='department',
        ),
        migrations.RemoveField(
            model_name='module',
            name='lecturer',
        ),
        migrations.RemoveField(
            model_name='module',
            name='module_descriptor',
        ),
        migrations.RemoveField(
            model_name='module',
            name='name',
        ),
        migrations.RemoveField(
            model_name='module',
            name='natural_Sciences_History',
        ),
        migrations.RemoveField(
            model_name='module',
            name='sub_category',
        ),
        migrations.RemoveField(
            model_name='module',
            name='term',
        ),
        migrations.RemoveField(
            model_name='module',
            name='topic_pathway',
        ),
        migrations.RemoveField(
            model_name='module',
            name='year',
        ),
    ]
