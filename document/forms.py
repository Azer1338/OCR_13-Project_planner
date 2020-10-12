from cloudinary.forms import CloudinaryFileField
from django import forms

from .models import ContributorDeliverable, Document, Deliverable


class AddDocumentToDeliverableForm(forms.ModelForm):
    link = CloudinaryFileField(
        options={
            'crop': 'thumb',
            'width': 200,
            'height': 200,
            'folder': 'link'
        },
    )

    class Meta:
        model = Document
        fields = [
            'name',
            'deliverable',
            'link'
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