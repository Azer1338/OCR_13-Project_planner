from django.db import models
from django.utils import timezone

from accounts.models import ProjectPlannerUser


class Project(models.Model):
    # Choices
    STATUS = [
        ('NEW', 'Just created'),
        ('ON GOING', 'On going'),
        ('FINISHED', 'Finished'),
        ('DELETED', 'Deleted'),
    ]

    name = models.CharField(max_length=100, unique=True)
    creationDate = models.DateField(default=timezone.now)
    dueDate = models.DateField(default=timezone.now)
    deletionDate = models.DateField(default=timezone.now)
    closureDate = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS,
                              default="NEW")
    advancement = models.FloatField(default=1)
    description = models.CharField(max_length=150, unique=False,
                                   default="No description yet")
    # Many Project to many ProjectPlannerUser relationship
    contributor = models.ManyToManyField('accounts.ProjectPlannerUser',
                                         through='ContributorProject',
                                         through_fields=('project',
                                                         'projectPlannerUser')
                                         )

    def __str__(self):
        return self.name


class ContributorProject(models.Model):
    # Choices
    ROLE = [
        ('PM', 'Project Manager'),
        ('CONTRIB', 'Contributor'),
    ]
    addingDate = models.DateField(default=timezone.now)
    removingDate = models.DateField(default=timezone.now)
    permission = models.CharField(max_length=100, choices=ROLE,
                                  default='Project Manager')
    # Many Project to many ProjectPlannerUser relationship
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    projectPlannerUser = models.ForeignKey('accounts.ProjectPlannerUser',
                                           on_delete=models.CASCADE)



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
    projectPlannerUser = models.ForeignKey('accounts.ProjectPlannerUser',
                                           related_name='contributor_deliverable',
                                           on_delete=models.CASCADE)

    def __str__(self):
        return str(self.projectPlannerUser)
