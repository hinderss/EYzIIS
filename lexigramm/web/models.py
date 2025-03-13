import uuid
from django.db import models
from django.db.models import PROTECT

from alalyzer import analyzer


class UploadedFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.name


class Word(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    word = models.CharField(max_length=64)
    lemma = models.CharField(max_length=64)
    pos = models.CharField(max_length=8)
    tag = models.CharField(max_length=8)
    suffixes = models.JSONField(null=True)
    file = models.ForeignKey(UploadedFile, on_delete=PROTECT, null=True)

    @property
    def part_of_speech(self):
        return analyzer.explain_pos(self.pos)

    @property
    def tag_explained(self):
        return analyzer.explain_tag(self.tag)

    @property
    def lemma_stem(self):
        return analyzer.stem(self.lemma)
