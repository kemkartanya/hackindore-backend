from django.db import models


class TimeStampedModelMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeletableModelMixin(models.Model):
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True