# Generated by Django 5.1.6 on 2025-04-24 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_remove_comment_created_date_remove_comment_user_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Название'),
        ),
    ]
