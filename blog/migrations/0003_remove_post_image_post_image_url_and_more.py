# Generated by Django 5.1.7 on 2025-04-04 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_telegraph_path_post_telegraph_url_post_views_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.AddField(
            model_name='post',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='telegraph_page_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
