# Generated by Django 5.0.4 on 2024-05-07 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_otpcode_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcode',
            name='code',
            field=models.CharField(max_length=4),
        ),
    ]
