# Generated by Django 3.0.3 on 2020-04-04 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cbvpro', '0002_auto_20200404_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbvpro.UserGroup'),
        ),
    ]