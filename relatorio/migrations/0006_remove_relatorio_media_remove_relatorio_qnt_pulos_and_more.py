# Generated by Django 4.2.4 on 2023-09-14 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_acao_options'),
        ('relatorio', '0005_relatorio_qnt_pulos_relatorio_qnt_respostas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relatorio',
            name='media',
        ),
        migrations.RemoveField(
            model_name='relatorio',
            name='qnt_pulos',
        ),
        migrations.RemoveField(
            model_name='relatorio',
            name='qnt_respostas',
        ),
        migrations.RemoveField(
            model_name='relatorio',
            name='respostas',
        ),
        migrations.AddField(
            model_name='relatorio',
            name='arquivo',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Arquivo'),
        ),
        migrations.AddField(
            model_name='relatorio',
            name='coordenadoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.coordenadoria'),
        ),
        migrations.AddField(
            model_name='relatorio',
            name='sistema',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.sistema'),
        ),
    ]
