# Generated by Django 4.2.20 on 2025-03-10 22:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("verses", "0003_verse_customid_index_verse_embedding_index_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="verse",
            name="tokens",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
