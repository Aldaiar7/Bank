# Generated by Django 4.0.4 on 2022-04-15 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('used_at', models.DateTimeField()),
                ('sum', models.PositiveIntegerField()),
                ('status', models.BooleanField(choices=[(1, 'not active'), (2, 'activated'), (3, 'expired')], default=2)),
            ],
        ),
    ]