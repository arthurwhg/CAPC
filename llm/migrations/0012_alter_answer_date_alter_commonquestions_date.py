# Generated by Django 4.2.18 on 2025-01-29 23:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("llm", "0011_remove_answer_commentn"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="date",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="commonquestions",
            name="date",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
