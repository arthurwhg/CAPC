# Generated by Django 4.2.18 on 2025-02-01 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("llm", "0012_alter_answer_date_alter_commonquestions_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="question",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to="llm.commonquestions",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="date",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="comment",
            name="parent_comment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="llm.comment",
            ),
        ),
    ]
