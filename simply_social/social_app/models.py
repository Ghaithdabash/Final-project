# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
import datetime
from datetime import datetime, timedelta
from django.utils.timesince import timesince


class Follower(models.Model):
    id = models.BigAutoField(primary_key=True)
    followerid = models.BigIntegerField()
    userid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='userid')
    connected = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'Follower'


class Following(models.Model):
    id = models.BigAutoField(primary_key=True)
    followingid = models.BigIntegerField()
    userid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='userid')

    class Meta:
        managed = False
        db_table = 'Following'


class Reply(models.Model):
    id = models.BigAutoField(primary_key=True)
    reply = models.CharField(max_length=256)
    textid = models.ForeignKey('Post', models.DO_NOTHING, db_column='textid',related_name='comments')
    userid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='userid')
    date = models.DateTimeField()
    likecount = models.IntegerField(blank=True, null=True)
    profileid = models.ForeignKey('Userprofile', models.DO_NOTHING, db_column='profileid')

    def get_current_date(self):
      now = datetime.now()
      try:
          difference = now - self.date
      except:
          return self.date

      if difference <= timedelta(minutes=1):
          return 'Just Now'
      return '%(time)s' % {'time': timesince(self.date).split(', ')[0]}

    class Meta:
        managed = False
        db_table = 'Reply'


class Replylike(models.Model):
    id = models.BigAutoField(primary_key=True)
    replyid = models.ForeignKey(Reply, models.DO_NOTHING, db_column='replyid')
    userid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='userid')

    class Meta:
        managed = False
        db_table = 'Replylike'


class Texlike(models.Model):
    id = models.BigAutoField(primary_key=True)
    textid = models.ForeignKey('Post', models.DO_NOTHING, db_column='textid')
    userid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='userid')

    class Meta:
        managed = False
        db_table = 'Texlike'


class Userprofile(models.Model):
    id = models.BigAutoField(primary_key=True)
    profilepic = models.ImageField(max_length=256, blank=True, null=True, upload_to='profile_pics')
    bio = models.CharField(max_length=256, blank=True, null=True)
    userid = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='userid')
    postcount = models.IntegerField(blank=True, null=True)
    followercount = models.IntegerField(blank=True, null=True)
    followingcount = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10)
    status = models.NullBooleanField()
    portfolio = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Userprofile'


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

    def get_absolute_url(self):
        return reverse("user_update", kwargs={'pk':self.pk})

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


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=256, blank=True, null=True)
    userid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='userid')
    expand = models.BooleanField()
    date = models.DateTimeField()
    likecount = models.IntegerField(blank=True, null=True)
    photo = models.ImageField(max_length=256, blank=True, null=True, upload_to='posts_images')
    video = models.CharField(max_length=256, blank=True, null=True)
    profileid = models.ForeignKey(Userprofile, models.DO_NOTHING, db_column='profileid')

    def get_absolute_url(self):
        return reverse("home", kwargs={'pk':self.pk})

    def get_current(self):
       now = datetime.now()
       try:
           difference = now - self.date
       except:
           return self.date
       if difference <= timedelta(minutes=1):
           try:
               return "justnow"
           except:
               return self.date
       return '%(time)s ago' % {'time': timesince(self.date).split(', ')[0]}

    class Meta:
        managed = False
        db_table = 'post'


class SocialAuthAssociation(models.Model):
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'social_auth_association'
        unique_together = (('server_url', 'handle'),)


class SocialAuthCode(models.Model):
    email = models.CharField(max_length=254)
    code = models.CharField(max_length=32)
    verified = models.BooleanField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'social_auth_code'
        unique_together = (('email', 'code'),)


class SocialAuthNonce(models.Model):
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=65)

    class Meta:
        managed = False
        db_table = 'social_auth_nonce'
        unique_together = (('server_url', 'timestamp', 'salt'),)


class SocialAuthPartial(models.Model):
    token = models.CharField(max_length=32)
    next_step = models.SmallIntegerField()
    backend = models.CharField(max_length=32)
    data = models.TextField()
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'social_auth_partial'


class SocialAuthUsersocialauth(models.Model):
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    extra_data = models.TextField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'social_auth_usersocialauth'
        unique_together = (('provider', 'uid'),)
