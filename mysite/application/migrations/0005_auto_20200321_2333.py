# Generated by Django 3.0.3 on 2020-03-21 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0004_article'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('content', mdeditor.fields.MDTextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question2_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Question2',
                'verbose_name_plural': 'Question2',
            },
        ),
        migrations.DeleteModel(
            name='Article',
        ),
    ]