# Generated by Django 5.0.7 on 2024-08-22 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0002_comment_create_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='text',
            new_name='comment',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='author',
            new_name='name',
        ),
    ]
