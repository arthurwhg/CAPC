# Generated by Django 4.2.18 on 2025-03-06 22:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("llm", "0015_alter_comment_question"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="by",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
