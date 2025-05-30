# Generated by Django 4.2.20 on 2025-03-10 22:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("verses", "0002_alter_verse_embedding"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="verse",
            index=models.Index(fields=["customId"], name="customId_index"),
        ),
        migrations.AddIndex(
            model_name="verse",
            index=models.Index(fields=["embedding"], name="embedding_index"),
        ),
        migrations.AddIndex(
            model_name="verse",
            index=models.Index(fields=["topic"], name="topic_index"),
        ),
        migrations.AddIndex(
            model_name="verse",
            index=models.Index(fields=["id"], name="id_index"),
        ),
    ]
