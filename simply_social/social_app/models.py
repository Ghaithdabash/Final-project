# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Follower(models.Model):
    id = models.BigIntegerField(primary_key=True)
    followerid = models.BigIntegerField()
    userid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='userid')
    connected = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'Follower'


class Following(models.Model):
    id = models.BigIntegerField(primary_key=True)
    followingid = models.BigIntegerField()
    userid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='userid')

    class Meta:
        managed = False
        db_table = 'Following'


class Photo(models.Model):
    id = models.BigIntegerField(primary_key=True)
    photo = models.ImageField(max_length=256)
    userid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='userid')
    textid = models.ForeignKey('Text', models.DO_NOTHING, db_column='textid')

    class Meta:
        managed = False
        db_table = 'Photo'


class Reply(models.Model):
    id = models.BigIntegerField(primary_key=True)
    reply = models.CharField(max_length=256)
    textid = models.ForeignKey('Text', models.DO_NOTHING, db_column='textid')
    userid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='userid')
    date = models.DateTimeField()
    likecount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Reply'


class Replylike(models.Model):
    id = models.BigIntegerField(primary_key=True)
    replyid = models.ForeignKey(Reply, models.DO_NOTHING, db_column='replyid')
    userid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='userid')

    class Meta:
        managed = False
        db_table = 'Replylike'


class Texlike(models.Model):
    id = models.BigIntegerField(primary_key=True)
    textid = models.ForeignKey('Text', models.DO_NOTHING, db_column='textid')
    userid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='userid')

    class Meta:
        managed = False
        db_table = 'Texlike'


class Text(models.Model):
    id = models.BigIntegerField(primary_key=True)
    text = models.CharField(max_length=256)
    userid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='userid')
    expand = models.BooleanField()
    date = models.DateTimeField()
    likecount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Text'


class Userprofile(models.Model):
    id = models.BigIntegerField(primary_key=True)
    profilepic = models.ImageField(max_length=256, blank=True, null=True)
    portfolio_field = models.CharField(db_column='portfolio ', max_length=256, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    bio = models.CharField(max_length=256, blank=True, null=True)
    userid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='userid')
    satus = models.BooleanField()
    postcount = models.IntegerField()
    followercount = models.IntegerField()
    followingcount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Userprofile'


class Video(models.Model):
    id = models.BigIntegerField(primary_key=True)
    video = models.CharField(max_length=256)
    userid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='userid')
    textid = models.ForeignKey(Text, models.DO_NOTHING, db_column='textid')

    class Meta:
        managed = False
        db_table = 'Video'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
