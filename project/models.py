from django.db import models
from django.utils import timezone


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