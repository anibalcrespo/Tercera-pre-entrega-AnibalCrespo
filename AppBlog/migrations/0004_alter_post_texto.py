# Generated by Django 4.2.3 on 2023-07-22 08:22

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppBlog', '0003_alter_post_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='texto',
            field=ckeditor.fields.RichTextField(),
        ),
    ]