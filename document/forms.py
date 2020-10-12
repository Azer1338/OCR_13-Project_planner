from cloudinary.forms import CloudinaryFileField
from django import forms

from document.models import Document


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
