# Generated by Django 5.0.2 on 2024-02-19 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=1000, verbose_name='пароль'),
        ),
    ]
