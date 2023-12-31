# Generated by Django 4.1 on 2023-07-15 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_remove_category_parent_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100, verbose_name='Модель машини')),
                ('content', models.TextField(max_length=300, verbose_name='Відгук')),
                ('author', models.CharField(max_length=100, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Коментар',
                'verbose_name_plural': 'Коментарі',
            },
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['model'], name='shop_commen_model_3ef185_idx'),
        ),
    ]
