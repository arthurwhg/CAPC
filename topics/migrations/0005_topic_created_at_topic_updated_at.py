# Generated by Django 4.2.20 on 2025-03-10 05:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("topics", "0004_alter_topic_book_alter_topic_video"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="topic",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
