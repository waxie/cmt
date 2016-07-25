
from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from tagging.fields import TagField


class ModelExtension(models.Model):
    tags = TagField()
    created_on = CreationDateTimeField()
    updated_on = ModificationDateTimeField()
    note = models.TextField(blank=True)

    class Meta:
        abstract = True