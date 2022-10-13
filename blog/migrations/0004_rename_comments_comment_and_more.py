# Generated by Django 4.0 on 2022-10-12 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comments_comments_blog_commen_created_ad0231_idx'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
        migrations.RemoveIndex(
            model_name='comment',
            name='blog_commen_created_ad0231_idx',
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['created'], name='blog_commen_created_0e6ed4_idx'),
        ),
    ]