# Generated by Django 4.2.18 on 2025-01-27 21:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("llm", "0002_alter_answer_id_alter_comment_id_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Tabc",
        ),
        migrations.DeleteModel(
            name="Test",
        ),
    ]
