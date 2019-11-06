# Generated by Django 2.2.6 on 2019-11-06 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0003_auto_20191009_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=30)),
                ('first_name', models.CharField(max_length=30)),
                ('birth', models.DateField()),
                ('street_adress', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=70)),
                ('certificate', models.BooleanField(default=False)),
                ('payment', models.BooleanField(default=False)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Club')),
            ],
        ),
    ]