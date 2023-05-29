# Generated by Django 4.2.1 on 2023-05-29 10:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_rename_cpu_history_cpuhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemoryHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('memory_percentage_used', models.FloatField(max_length=5)),
                ('dev_date', models.DateField(default=datetime.date.today)),
                ('dev_time', models.TimeField(default=datetime.datetime.now)),
                ('dev_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.generalinfo')),
            ],
            options={
                'verbose_name': 'Memory History',
                'verbose_name_plural': 'Memory History',
            },
        ),
    ]
