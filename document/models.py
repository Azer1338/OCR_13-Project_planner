from cloudinary.models import CloudinaryField
from django.db import models
from django.utils import timezone

from accounts.models import ProjectPlannerUser


class Deliverable(models.Model):
    # Choices
    STATUS = [
        ('NEW', 'Just created'),
        ('APPROVAL ON GOING', 'Approval on going'),
        ('APPROVED', 'Approved'),
        ('DELETED', 'Deleted'),
    ]
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=251, unique=False)
    addingDate = models.DateField(default=timezone.now)
    dueDate = models.DateField(default=timezone.now)
    closureDate = models.DateField(default=timezone.now)
    deletionDate = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS, default='NEW')
    progression = models.FloatField(max_length=505, unique=False, default=1)
    # One Project to many Deliverable relationship
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE)
    # Many Deliverable to many ProjectPlannerUser relationship
    contributor = models.ManyToManyField(ProjectPlannerUser,
                                         through='ContributorDeliverable',
                                         through_fields=('deliverable',
                                                         'projectPlannerUser'))

    def __str__(self):
        return self.name


class Document(models.Model):
    name = models.CharField(max_length=100, unique=True)
    loadingDate = models.DateField(default=timezone.now)
    link = CloudinaryField('link')
    # One Deliverable to many Document relationship
    deliverable = models.ForeignKey(Deliverable, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ContributorDeliverable(models.Model):
    # Choices
    FUNCTION = [
        ('AUTHOR', 'Author'),
        ('VALIDATOR', 'Validator'),
        ('COLLABORATOR', 'Collaborator'),
    ]
    FEEDBACK = [
        ('NOTKNOWN', 'Not Known'),
        ('AGREED', 'Agreed'),
        ('DISAGREED', 'Disagreed'),
    ]
    function = models.CharField(max_length=20,
                                choices=FUNCTION,
                                default='Author')
    feedback = models.CharField(max_length=20,
                                choices=FEEDBACK,
                                default='Not Known')
    comment = models.CharField(max_length=150)
    # Many Deliverable to many ProjectPlannerUser relationship
    deliverable = models.ForeignKey(Deliverable,
                                    related_name='contributor_deliverable',
                                    on_delete=models.CASCADE)
    projectPlannerUser = models.ForeignKey(ProjectPlannerUser,
                                           related_name='contributor_deliverable',
                                           on_delete=models.CASCADE)

    def __str__(self):
        return str(self.projectPlannerUser)