# Generated by Django 4.1.2 on 2022-10-16 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teachers', '0001_initial'),
        ('classes', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='teachers',
            field=models.ManyToManyField(to='teachers.teacherprofile'),
        ),
    ]