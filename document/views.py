from django.contrib import messages
from django.shortcuts import render, redirect
import cloudinary
import cloudinary.uploader
import cloudinary.api

from document.forms import AddDocumentToDeliverableForm
from main.settings import env
from project.models import Deliverable


def add_document_to_deliverable_view(request, deliverable_id):
    """
    Link a document to the deliverable.
    :param deliverable_id:
    :param request:
    :return:
    """
    # API config
    cloudinary.config(
        cloud_name=env.str('CLOUDINARY_CONFIG_CLOUD_NAME'),
        api_key=env.str('CLOUDINARY_CONFIG_API_KEY'),
        api_secret=env.str('CLOUDINARY_CONFIG_API_SECRET'),
        secure=True
    )
    # Gather information
    deliverable = Deliverable.objects.get(id=deliverable_id)

    # Form =

    context = {
        'deliverable': deliverable,
        'add_document_form': AddDocumentToDeliverableForm(),
    }

    # In POST case
    if request.method == 'POST':
        form = AddDocumentToDeliverableForm(request.POST, request.FILES)
        form.deliverable = deliverable_id
        if form.is_valid():
            # Save the form
            form.save()

            # Message
            messages.success(request, 'Document added!')

            # Go to the deliverable homepage
            return redirect('deliverable:displayDeliverable',
                            deliverable_id=deliverable.id)
        else:
            # Message
            messages.warning(request, 'Some fields are not correct!')

    return render(request, 'deliverable/addDocumentToDeliverable.html',
                  context)
