# Generated by Django 2.2.1 on 2019-07-26 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plays', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UploadFile',
            new_name='Photo',
        ),
    ]
