from django import forms

from deliverable.models import Deliverable
from .models import Project, ContributorProject


class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
            'description'
        ]


class AddMemberToProjectForm(forms.ModelForm):
    class Meta:
        model = ContributorProject
        fields = [
            'projectPlannerUser'
        ]
        labels = {
            'projectPlannerUser': 'New Member name'
        }


class AddDeliverableToProjectForm(forms.ModelForm):
    class Meta:
        model = Deliverable
        fields = [
            'name',
            'description',
            'dueDate'
        ]


class ModifyProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'description',
            'dueDate'
        ]