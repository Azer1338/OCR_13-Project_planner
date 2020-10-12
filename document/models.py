from cloudinary.models import CloudinaryField
from django.db import models
from django.utils import timezone

from project.models import Deliverable


class Document(models.Model):
    name = models.CharField(max_length=100, unique=True)
    loadingDate = models.DateField(default=timezone.now)
    link = CloudinaryField('link')
    # One Deliverable to many Document relationship
    deliverable = models.ForeignKey(Deliverable, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
