# Generated by Django 2.1.3 on 2018-11-14 10:37

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid
import votetrackr_api.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('UID', models.UUIDField(db_column='UID', default=uuid.uuid4, editable=False)),
                ('name', models.TextField(blank=True, db_column='Name', null=True)),
                ('district', models.IntegerField(blank=True, db_column='District', null=True)),
            ],
            options={
                'db_table': 'Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('BID', models.CharField(db_column='BID', default=votetrackr_api.models.create_random_id, editable=False, max_length=12, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, db_column='Description')),
                ('date_introduced', models.DateField(db_column='DateIntroduced', default=datetime.date.today)),
                ('status', models.TextField(blank=True, choices=[('P', 'Passed'), ('R', 'Rejected'), ('OTF', 'On the Floor'), ('IC', 'In committee')], db_column='Status')),
                ('voted_on', models.BooleanField(blank=True, db_column='VotedOn', null=True)),
                ('congress_num', models.IntegerField(blank=True, db_column='CongressN', null=True)),
                ('chamber', models.CharField(blank=True, choices=[('S', 'Senate'), ('H', 'House of Representatives')], db_column='Chamber', max_length=10)),
                ('session', models.IntegerField(blank=True, db_column='Session', null=True)),
                ('date_voted', models.DateField(blank=True, db_column='DateVoted', default=datetime.date.today)),
                ('url', models.URLField(blank=True, db_column='URL', null=True)),
            ],
            options={
                'db_table': 'Bills',
            },
        ),
        migrations.CreateModel(
            name='Legislator',
            fields=[
                ('LID', models.CharField(db_column='LID', default=votetrackr_api.models.create_random_id, editable=False, max_length=12, primary_key=True, serialize=False)),
                ('fullname', models.CharField(blank=True, db_column='FullName', max_length=255)),
                ('senator', models.BooleanField(blank=True, db_column='isSenator', null=True)),
                ('affiliation', models.TextField(blank=True, choices=[('D', 'Democrat'), ('R', 'Republican'), ('I', 'Independent'), ('O', 'Other')], db_column='Affiliation', null=True)),
                ('dwnominate', models.FloatField(blank=True, db_column='DWNominate', null=True)),
                ('url', models.URLField(blank=True, db_column='URL', null=True)),
            ],
            options={
                'db_table': 'Legislators',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('VID', models.UUIDField(db_column='ID', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('vote', models.CharField(blank=True, choices=[('Y', 'Yea'), ('N', 'Nay'), ('A', 'Abstain')], max_length=1)),
                ('bill', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='votetrackr_api.Bill')),
                ('legislator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='votetrackr_api.Legislator')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Votes',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='followed',
            field=models.ManyToManyField(blank=True, related_name='followed', to='votetrackr_api.Legislator'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='matched',
            field=models.ManyToManyField(blank=True, related_name='matched', to='votetrackr_api.Legislator'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]