# Generated by Django 5.1.6 on 2025-05-22 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0069_testattempt_correct_answers_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testattempt',
            name='total_questions_at_submission',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Tổng số câu khi nộp'),
        ),
    ]
