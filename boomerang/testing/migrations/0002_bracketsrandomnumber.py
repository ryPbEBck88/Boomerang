# Generated by Django 3.2.16 on 2024-09-05 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BracketsRandomNumber',
            fields=[
                ('randomnumber_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='testing.randomnumber')),
            ],
            bases=('testing.randomnumber',),
        ),
    ]
