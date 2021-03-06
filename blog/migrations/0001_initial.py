# Generated by Django 2.1 on 2018-09-26 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=300)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, default='default.png', upload_to='')),
                ('body', models.TextField(db_index=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
