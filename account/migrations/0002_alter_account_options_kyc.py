# Generated by Django 5.0.1 on 2024-01-13 23:30

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ['-updated_at']},
        ),
        migrations.CreateModel(
            name='KYC',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('full_name', models.CharField(max_length=1000)),
                ('image', models.ImageField(default='default.jpg', upload_to='kyc')),
                ('marrital_status', models.CharField(choices=[('married', 'Married'), ('single', 'Single'), ('other', 'Other')], max_length=40)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=40)),
                ('identity_type', models.CharField(choices=[('national_id_card', 'National ID Card'), ('drivers_licence', 'Drives Licence'), ('international_passport', 'International Passport')], max_length=140)),
                ('identity_image', models.ImageField(blank=True, null=True, upload_to='kyc')),
                ('date_of_birth', models.DateField()),
                ('signature', models.ImageField(upload_to='kyc')),
                ('country', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=1000)),
                ('fax', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
    ]
