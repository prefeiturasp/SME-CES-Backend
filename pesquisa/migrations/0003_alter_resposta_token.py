# Generated by Django 4.2.4 on 2023-09-13 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pesquisa', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resposta',
            name='token',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pesquisa.token'),
        ),
    ]
