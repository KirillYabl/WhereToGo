# Generated by Django 4.1.3 on 2022-11-22 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='place',
            options={'verbose_name': 'место', 'verbose_name_plural': 'места'},
        ),
        migrations.CreateModel(
            name='PlaceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_image', models.ImageField(upload_to='', verbose_name='картинка места')),
                ('image_order', models.PositiveSmallIntegerField(help_text='порядок от меньшего к большему, т.е. 1 покажется первой', verbose_name='порядок отображения')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='places.place')),
            ],
            options={
                'verbose_name': 'изображение места',
                'verbose_name_plural': 'изображения места',
                'unique_together': {('place', 'image_order')},
            },
        ),
    ]
