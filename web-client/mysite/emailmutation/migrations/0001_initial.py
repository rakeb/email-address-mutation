# Generated by Django 2.2.3 on 2019-10-31 04:54

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllShadowEmail',
            fields=[
                ('shadow_email', models.CharField(max_length=500, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='AllVipEmail',
            fields=[
                ('vip_email', models.CharField(max_length=500, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='HashedEmailTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_address', models.CharField(max_length=500)),
                ('to_address', models.CharField(max_length=500)),
                ('last_n_email_hash', jsonfield.fields.JSONField()),
                ('mID', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MarkVerificationStatus',
            fields=[
                ('message_id', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MutationParam',
            fields=[
                ('email_address', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=500)),
                ('shadow_list', jsonfield.fields.JSONField()),
            ],
        ),
    ]
