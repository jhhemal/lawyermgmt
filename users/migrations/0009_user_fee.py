# Generated by Django 3.1.3 on 2021-01-04 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210104_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fee',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Consultaion Fee'),
        ),
    ]