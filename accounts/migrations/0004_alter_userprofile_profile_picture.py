# Generated by Django 4.2.7 on 2023-11-19 14:20

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.UserProfile.profile_pic_upload_path),
        ),
    ]
