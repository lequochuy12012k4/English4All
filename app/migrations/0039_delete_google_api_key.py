# Generated by Django 5.1.6 on 2025-03-24 03:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_rename_googleapi_key_google_api_key'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Google_API_Key',
        ),
    ]
