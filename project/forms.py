from django import forms

from project.models import Project, ContributorProject, Deliverable, ContributorDeliverable


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

class AddContributorToDeliverableForm(forms.ModelForm):
    class Meta:
        model = ContributorDeliverable
        fields = [
            'projectPlannerUser',
            'function'
        ]
        labels = {
            'projectPlannerUser': 'New contributor email'
        }


class UpdateContributorComment(forms.ModelForm):
    class Meta:
        model = ContributorDeliverable
        fields = [
            'feedback',
            'comment',
        ]


class ModifyDeliverableContentForm(forms.ModelForm):
    class Meta:
        model = Deliverable
        fields = [
            'description',
            'dueDate'
        ]
