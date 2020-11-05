from django.db import models

from jsonfield import JSONField


class MutationParam(models.Model):
    email_address = models.CharField(max_length=500, primary_key=True)
    password = models.CharField(max_length=500)
    shadow_list = JSONField()


class AllShadowEmail(models.Model):
    shadow_email = models.CharField(max_length=500, primary_key=True)


class AllVipEmail(models.Model):
    vip_email = models.CharField(max_length=500, primary_key=True)


class HashedEmailTable(models.Model):
    from_address = models.CharField(max_length=500)
    to_address = models.CharField(max_length=500)
    last_n_email_hash = JSONField()
    mID = models.IntegerField()


class MarkVerificationStatus(models.Model):
    message_id = models.CharField(max_length=500, primary_key=True)
    status = models.BooleanField(default=False)
