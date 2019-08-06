# Generated by Django 2.2.4 on 2019-08-06 07:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0004_auto_20190806_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountingDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='accountDocument',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='Transaction', to='accounting.AccountingDocument'),
            preserve_default=False,
        ),
    ]