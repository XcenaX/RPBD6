# Generated by Django 4.1.3 on 2022-12-02 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_student_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='ru_name',
            field=models.TextField(default=''),
        ),
    ]