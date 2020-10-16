from cloudinary.models import CloudinaryField
from django.db import models
from django.utils import timezone


class Document(models.Model):
    name = models.CharField(max_length=100, unique=True)
    loadingDate = models.DateField(default=timezone.now)
    link = CloudinaryField('link')
    # One Deliverable to many Document relationship
    deliverable = models.ForeignKey('project.Deliverable',
                                    on_delete=models.CASCADE)

    def __str__(self):
        return self.name
