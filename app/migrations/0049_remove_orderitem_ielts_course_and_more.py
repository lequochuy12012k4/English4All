# Generated by Django 5.1.6 on 2025-03-24 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0048_orderitem_ielts_course_orderitem_thptqg_course_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='ielts_course',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='thptqg_course',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='toeic_course',
        ),
        migrations.AddField(
            model_name='course',
            name='course_type',
            field=models.CharField(choices=[('TOEIC', 'TOEIC'), ('IELTS', 'IELTS'), ('THPTQG', 'THPTQG')], default='TOEIC', max_length=20),
        ),
    ]
