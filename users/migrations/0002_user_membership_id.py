# Generated by Django 3.1.3 on 2020-12-02 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='membership_id',
            field=models.TextField(blank=True, max_length=15, null=True, verbose_name='Bar Membership ID'),
        ),
    ]
