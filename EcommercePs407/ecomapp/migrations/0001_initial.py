# Generated by Django 5.0.6 on 2024-12-19 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=100)),
                ('mob', models.CharField(max_length=20)),
                ('msg', models.CharField(max_length=300)),
            ],
        ),
    ]
