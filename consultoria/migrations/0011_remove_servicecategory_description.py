# Generated by Django 5.1.2 on 2025-02-10 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultoria', '0010_offer_alter_news_description_alter_news_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicecategory',
            name='description',
        ),
    ]
