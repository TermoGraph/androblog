# Generated by Django 2.1 on 2018-09-30 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20180930_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='app_type',
            field=models.CharField(blank=True, db_index=True, max_length=100),
        ),
    ]
