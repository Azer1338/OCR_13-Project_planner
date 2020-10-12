from django.contrib import messages
from django.shortcuts import render, redirect
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.utils import timezone

from accounts.function_for_accounts import send_notifications_to_contributor
from project.function_for_project import contributor_is_not_already_in_the_list
from project_planner.settings import env
from .forms import AddDocumentToDeliverableForm, \
    AddContributorToDeliverableForm, \
    UpdateContributorComment, ModifyDeliverableContentForm
from .function_for_deliverable import define_deliverable_progression
from .models import Deliverable, Document, ContributorDeliverable


def display_deliverable_view(request, deliverable_id):
    """
    Display the main page of a document.
    :param request:
    :param deliverable_id:
    :return:
    """
    # Gather information
    define_deliverable_progression(deliverable_id)
    deliverable = Deliverable.objects.get(id=deliverable_id)
    project = deliverable.project
    documents = Document.objects.filter(deliverable=deliverable_id)
    contributors = ContributorDeliverable.objects. \
        filter(deliverable=deliverable_id)
    contributors_length = len(contributors)

    # Generate forms
    add_contributor_form = AddContributorToDeliverableForm()
    update_contributor_form = UpdateContributorComment()

    # Check if the user is a contributor of the deliverable
    current_user_list = ContributorDeliverable.objects. \
        filter(deliverable=deliverable, projectPlannerUser=request.user)
    if len(current_user_list) == 0:
        current_user_role = "Not a Contributor"
        current_user = "John DOE"
    else:
        current_user_role = current_user_list[0].function
        current_user = current_user_list[0]

    # Create a contributors list
    contributors = ContributorDeliverable.objects. \
        filter(deliverable=deliverable_id)
    contributor_list = []
    for member in contributors:
        contributor_list.append(member.projectPlannerUser.email)

    # Generate a context
    context = {
        'project': project,
        'deliverable': deliverable,
        'documents': documents,
        'contributors': contributors,
        'addContributorForm': add_contributor_form,
        'updateContributorForm': update_contributor_form,
        'user': request.user,
        'current_user': current_user,
        'user_function': current_user_role,
        'contributors_length': contributors_length
    }

    # Render a flex or frozen template
    if deliverable.status != "APPROVED":
        # Flex template - with form
        return render(request,
                      'deliverable/displayDeliverable.html', context)
    else:
        # Frozen template - without form
        return render(request,
                      'deliverable/displayDeliverableWithoutForms.html',
                      context)


def modify_deliverable_view(request, deliverable_id):
    """
    Modify the content of a deliverable.
    :param request:
    :param deliverable_id:
    :return:
    """
    # Gather information
    deliverable = Deliverable.objects.get(id=deliverable_id)

    if request.method == 'POST':
        # Gather information form a form
        form = ModifyDeliverableContentForm(request.POST)
        if form.is_valid():
            # Modify the Deliverable
            deliverable_description_updated = form.data['description']
            deliverable_due_date_updated = form.data['dueDate']
            deliverable.description = deliverable_description_updated
            deliverable.dueDate = deliverable_due_date_updated
            deliverable.save()

            # Message
            messages.success(request, 'Deliverable modified!')

            # Redirect to the project main page
            return redirect('deliverable:displayDeliverable',
                            deliverable_id=deliverable.id)
        else:
            # Message
            messages.warning(request, 'Some fields are not correct.')
    else:
        # Generate a form
        form = ModifyDeliverableContentForm()

    # Generate a context
    context = {
        'form': form,
        'deliverable': deliverable
    }

    return render(request, 'deliverable/modifyDeliverable.html', context)


def add_contributor_to_deliverable_view(request, deliverable_id):
    """
       Display the main page of a document.
       :param request:
       :param deliverable_id:
       :return:
       """

    # Gather information
    deliverable = Deliverable.objects.get(id=deliverable_id)
    # Create a contributors list
    contributors = ContributorDeliverable.objects. \
        filter(deliverable=deliverable_id)
    contributor_list = []
    for member in contributors:
        contributor_list.append(member.projectPlannerUser.email)

    # If a form is returned
    if request.method == 'POST':
        # Generate a form
        add_contributor_form = AddContributorToDeliverableForm(request.POST)

        # Check if user designed is not already a contributor
        member_designed = ProjectPlannerUser.objects. \
            get(id=add_contributor_form.data['projectPlannerUser'])
        already_in_the_list_check = contributor_is_not_already_in_the_list(member_designed,
                                                                           contributor_list)

        if add_contributor_form.is_valid() and not already_in_the_list_check:
            # Alert message
            messages.success(request, "User added as contributor")
            # Build an instance from model and save
            member_designed = ProjectPlannerUser.objects. \
                get(id=add_contributor_form.data['projectPlannerUser'])
            contributor_added = ContributorDeliverable(projectPlannerUser=member_designed,
                                                       function=add_contributor_form.data['function'],
                                                       deliverable=deliverable)
            contributor_added.save()

            # Collaborator always provide an positive agreement
            if contributor_added.function == 'COLLABORATOR':
                contributor_added.feedback = 'AGREED'
                contributor_added.save()

            # Message
            messages.success(request, 'Contributor added!')
        else:
            # Notifications
            messages.warning(request, "User already in the team")
    else:
        pass

    # Redirect to homepage
    return redirect('deliverable:displayDeliverable',
                    deliverable_id=deliverable.id)


def remove_contributor_from_deliverable_view(request, member_id):
    """
    Remove a team member from a project.
    :param member_id:
    :return:
    """

    # Gather project information
    member_to_remove = ContributorDeliverable.objects.get(id=member_id)
    deliverable_id = member_to_remove.deliverable.id

    # Remove member from contributor list
    member_to_remove.delete()

    # Message
    messages.success(request, 'Contributor removed!')

    # Redirect to homepage
    return redirect('deliverable:displayDeliverable',
                    deliverable_id=deliverable_id)


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


def update_contribution_feedback_to_deliverable_view(request, contributor_id):
    """
    Modify feedback and comment from a contributor to the current deliverable.
    :param request:
    :param contributor_id:
    :return:
    """
    # Gather information
    contributor = ContributorDeliverable.objects.get(id=contributor_id)

    # Validate the POST Method
    if request.method == 'POST':
        # Update contributor data
        if request.POST.get("feedback"):
            contributor.feedback = request.POST.get("feedback")
        if request.POST.get("comment"):
            contributor.comment = request.POST.get("comment")

        contributor.save()
        # Alert messagedjan
        messages.success(request,
                         "Feedback updated for : " + str(contributor.feedback))
    else:
        # Message
        messages.warning(request, 'Some fields are not correct!')

    # Redirect to homepage
    return redirect('deliverable:displayDeliverable',
                    deliverable_id=contributor.deliverable.id)


def check_and_release_deliverable_view(request, deliverable_id):
    """
    Release deliverable if it is ok for every contributors.
    :param request:
    :param deliverable_id:
    :return:
    """
    # Gather information
    deliverable = Deliverable.objects.get(id=deliverable_id)

    # Check the progression of the deliverable
    progression = define_deliverable_progression(deliverable_id)

    if progression >= 100:
        deliverable.status = "APPROVED"
        deliverable.closureDate = timezone.now()
        deliverable.save()

        # Email contributor
        send_notifications_to_contributor(deliverable)

        # Message
        messages.success(request, 'Deliverable finalized!')
    else:
        deliverable.status = 'APPROVAL ON GOING'
        deliverable.save()

    return redirect("deliverable:displayDeliverable",
                    deliverable_id=deliverable_id)