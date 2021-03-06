# Generated by Django 3.1.3 on 2021-01-04 08:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210104_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='Bio'),
        ),
        migrations.AddField(
            model_name='user',
            name='exp',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='Experience'),
        ),
        migrations.CreateModel(
            name='ExpertArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='Title')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
