# Generated by Django 2.2.1 on 2019-05-31 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_person_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='token',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
