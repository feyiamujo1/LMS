# Generated by Django 4.1.2 on 2022-10-16 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('body', models.TextField(blank=True, max_length=1040, null=True)),
                ('attachment', models.FileField(blank=True, max_length=20000, null=True, upload_to='files/')),
                ('given_on', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=True, max_length=2000, null=True)),
                ('attachment', models.FileField(blank=True, max_length=20000, null=True, upload_to='solutions/')),
                ('completed', models.BooleanField(default=False)),
                ('turn_in', models.BooleanField(default=False)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignments.assignment')),
            ],
        ),
    ]
