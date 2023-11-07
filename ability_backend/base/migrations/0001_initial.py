# Generated by Django 4.2.6 on 2023-11-07 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyRegister',
            fields=[
                ('company_id', models.AutoField(primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=255)),
                ('company_type', models.CharField(max_length=255)),
                ('phone', models.PositiveBigIntegerField(default=0)),
                ('email', models.CharField(max_length=255)),
                ('profile', models.CharField(max_length=255)),
                ('website', models.CharField(max_length=255)),
                ('license_no', models.PositiveBigIntegerField(default=0)),
                ('business_license', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='JobSeekerRegister',
            fields=[
                ('job_seeker_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=255)),
                ('phone', models.PositiveBigIntegerField(default=0)),
                ('email', models.CharField(max_length=255)),
                ('street_address_line1', models.CharField(max_length=255)),
                ('street_address_line2', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('highest_qualification', models.CharField(max_length=255)),
                ('institution', models.CharField(max_length=255)),
                ('cgpa', models.PositiveBigIntegerField(default=0)),
                ('resume', models.CharField(max_length=255)),
                ('experience_type', models.CharField(max_length=255)),
                ('job_title', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=255)),
                ('is_deleted', models.IntegerField(default=0)),
            ],
        ),
    ]
