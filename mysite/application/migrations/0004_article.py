# Generated by Django 3.0.3 on 2020-03-21 13:54

from django.db import migrations, models
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_auto_20200320_1344'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', mdeditor.fields.MDTextField()),
            ],
        ),
    ]
