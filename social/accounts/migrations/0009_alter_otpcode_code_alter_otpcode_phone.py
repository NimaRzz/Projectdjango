# Generated by Django 5.0.4 on 2024-05-06 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcode',
            name='code',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='otpcode',
            name='phone',
            field=models.CharField(max_length=11),
        ),
    ]
