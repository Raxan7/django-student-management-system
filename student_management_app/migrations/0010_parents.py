# Generated by Django 4.2.1 on 2024-04-12 07:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0009_alter_studentperformance_absences_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parents',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('child', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students')),
            ],
        ),
    ]
