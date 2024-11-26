# Generated by Django 4.2.1 on 2024-11-25 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testik', '0006_alter_test_cat'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='test',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tests', to='testik.category'),
        ),
        migrations.AddField(
            model_name='test',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='testik.tagtest'),
        ),
    ]
