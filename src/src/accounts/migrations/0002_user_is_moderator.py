# Generated by Django 4.1.7 on 2023-02-24 10:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_moderator",
            field=models.BooleanField(
                default=False,
                help_text="Может обогощать сообщения",
                verbose_name="Модератор",
            ),
        ),
    ]
