# Generated by Django 2.1.7 on 2019-03-08 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0001_initial'),
        ('collection', '0005_auto_20190307_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='primary_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_of', to='sources.Source'),
        ),
        migrations.AddField(
            model_name='collection',
            name='puzzles',
            field=models.ManyToManyField(related_name='puzzles_in', to='collection.Puzzle'),
        ),
    ]