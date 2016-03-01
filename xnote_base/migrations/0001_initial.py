# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('follow_time', models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permissions', models.ManyToManyField(related_name='related_portfolios', to='xnote_base.Permission')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_public', models.BooleanField(default=False)),
                ('post_type', models.CharField(default=b'normal', max_length=50, choices=[(b'normal', b'Normal'), (b'quick', b'Quick')])),
                ('title', models.CharField(max_length=100)),
                ('context', models.TextField()),
                ('publish_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Studentity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('student_id', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('field_of_study', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SuperConductor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('real_name', models.CharField(default=b'Unknown', max_length=100)),
                ('description', models.CharField(default=b'Nothing', max_length=1000)),
                ('url_name', models.CharField(max_length=100, null=True, blank=True)),
                ('is_formal', models.BooleanField(default=False)),
                ('profile_image', models.ImageField(null=True, upload_to=b'profile_image', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='xnote_base.Tag', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('superconductor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='xnote_base.SuperConductor')),
                ('national_id', models.CharField(max_length=100, null=True, blank=True)),
                ('sharif_mail_address', models.EmailField(max_length=254, null=True, blank=True)),
            ],
            bases=('xnote_base.superconductor',),
        ),
        migrations.CreateModel(
            name='SuperInstitution',
            fields=[
                ('superconductor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='xnote_base.SuperConductor')),
                ('name', models.CharField(max_length=100)),
            ],
            bases=('xnote_base.superconductor',),
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(blank=True, to='xnote_base.SuperConductor', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='event',
            field=models.ForeignKey(blank=True, to='xnote_base.Event', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='related_tags',
            field=models.ManyToManyField(to='xnote_base.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='follow',
            name='followed',
            field=models.ForeignKey(related_name='followers_follow_obj', to='xnote_base.SuperConductor'),
        ),
        migrations.AddField(
            model_name='event',
            name='conductor',
            field=models.ForeignKey(related_name='event_list', to='xnote_base.SuperConductor'),
        ),
        migrations.AddField(
            model_name='event',
            name='places',
            field=models.ManyToManyField(to='xnote_base.Place'),
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(to='xnote_base.Tag'),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('superinstitution_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='xnote_base.SuperInstitution')),
            ],
            bases=('xnote_base.superinstitution',),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('superinstitution_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='xnote_base.SuperInstitution')),
                ('is_department_group', models.BooleanField(default=False)),
            ],
            bases=('xnote_base.superinstitution',),
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('superinstitution_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='xnote_base.SuperInstitution')),
            ],
            bases=('xnote_base.superinstitution',),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('name',)]),
        ),
        migrations.AddField(
            model_name='superinstitution',
            name='members',
            field=models.ManyToManyField(to='xnote_base.Person', through='xnote_base.Membership'),
        ),
        migrations.AddField(
            model_name='studentity',
            name='person',
            field=models.ForeignKey(blank=True, to='xnote_base.Person', null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='follows',
            field=models.ManyToManyField(related_name='followers', through='xnote_base.Follow', to='xnote_base.SuperConductor'),
        ),
        migrations.AddField(
            model_name='person',
            name='interested_tags',
            field=models.ManyToManyField(to='xnote_base.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.OneToOneField(related_name='person', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='membership',
            name='institution',
            field=models.ForeignKey(related_name='membership_obj', to='xnote_base.SuperInstitution'),
        ),
        migrations.AddField(
            model_name='membership',
            name='person',
            field=models.ForeignKey(related_name='membership_obj', to='xnote_base.Person'),
        ),
        migrations.AddField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(related_name='following_follow_obj', to='xnote_base.Person'),
        ),
        migrations.AddField(
            model_name='event',
            name='invited',
            field=models.ManyToManyField(related_name='invite_list', to='xnote_base.Person'),
        ),
        migrations.AddField(
            model_name='studentity',
            name='department',
            field=models.ForeignKey(blank=True, to='xnote_base.Department', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='related_university',
            field=models.ForeignKey(related_name='xnote_base_group_related', to='xnote_base.University', null=True),
        ),
        migrations.AddField(
            model_name='department',
            name='related_university',
            field=models.ForeignKey(blank=True, to='xnote_base.University', null=True),
        ),
    ]
