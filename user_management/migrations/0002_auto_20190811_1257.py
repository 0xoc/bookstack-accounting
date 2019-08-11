# Generated by Django 2.2.4 on 2019-08-11 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='national_id',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='person_type',
            field=models.CharField(choices=[(0, 'نامشخص'), (1, 'حقیقی'), (2, 'حقوقی')], default=0, max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='telephone',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
