import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
import logging

from accounts.function_for_accounts import send_notifications_to_contributor
from accounts.models import ProjectPlannerUser
from document.models import Document
from project.forms import CreateProjectForm, ModifyProjectForm,\
    AddMemberToProjectForm, AddDeliverableToProjectForm, \
    AddContributorToDeliverableForm, UpdateContributorComment,\
    ModifyDeliverableContentForm
from project.function_for_project import define_project_advancement,\
    contributor_is_not_already_in_the_list, \
    define_deliverable_progression
from project.models import Project, Deliverable, ContributorProject,\
    ContributorDeliverable
from main.settings import env

# Get an instance of a logger
logger = logging.getLogger(__name__)

def index_view(request):
    """
    Return index page.
    :param request:
    :return:
    """
    
    logger.info('New search', exc_info=True, extra={
        # Optionally pass a request and we'll grab any information we can
        'request': request,
        })

    # return the index page
    return render(request, 'project/index.html')


def mentions_view(request):
    """
    Return mentions page.
    :param request:
    :return:
    """
    # return the mentions page
    return render(request, 'project/mentions.html')


def create_project_view(request):
    """
    Create a project based on user's description.
    :param request:
    :return:
    """
    # On POST method
    if request.method == 'POST':
        # Gather information into the right form
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            # Generate the project
            form.save()
            # Collect information from form
            project_created_name = form.data['name']
            # Modification on project and add a first deliverable
            project = Project.objects.get(name=project_created_name)
            project.contributor.add(request.user)
            first_deliverable = Deliverable(name='Project Frame of ' + project.name,
                                            description="Project details",
                                            project=project)
            first_deliverable.save()
            first_deliverable.contributor.add(request.user)

            # Email contributor
            send_notifications_to_contributor(project)
            # Message
            messages.success(request, 'Project created!')

            # Redirect to the project main page
            return redirect('project:displayProject',
                            project_id=project.id)
        else:
            # Message
            messages.warning(request, 'Some fields are not correct.')
    else:
        form = CreateProjectForm()

    return render(request, 'project/createProject.html', {'form': form})


def display_project_view(request, project_id):
    """
    Display the home page of a project.
    :param request:
    :param project_id:
    :return:
    """
    # Check the advancement
    define_project_advancement(project_id)
    # Gather the information about the project
    project = Project.objects.get(id=project_id)
    contributors = ContributorProject.objects.filter(project=project)
    contributors_length = len(contributors)

    # Check if the user is a contributor of the deliverable
    current_user = ContributorProject.objects.\
        filter(project=project, projectPlannerUser=request.user)
    if len(current_user) == 0:
        current_user_role = "Not a Contributor"
        current_user = "John DOE"
    else:
        current_user_role = current_user[0].permission
        current_user = current_user[0]

    # Generate a context
    context = {
        'project': project,
        'user': request.user,
        'current_user': current_user,
        'user_function': current_user_role,
        'contributors_length': contributors_length
    }

    # Render a flex or frozen template
    if project.status != "FINISHED":
        return render(request, 'project/displayProject.html', context)
    else:
        return render(request,
                      'project/displayProjectWithoutForms.html', context)


def modify_project_view(request, project_id):
    """
    Modify the content of a deliverable.
    :param request:
    :param project_id:
    :return:
    """
    # Gather information
    project = Project.objects.get(id=project_id)

    if request.method == 'POST':
        # Gather information from form
        form = ModifyProjectForm(request.POST)
        if form.is_valid():
            # Modify the project content
            project = Project.objects.get(id=project_id)
            project_description_updated = form.data['description']
            project_due_date_updated = form.data['dueDate']
            project.description = project_description_updated
            project.dueDate = project_due_date_updated
            project.save()

            # Message
            messages.success(request, 'Project modified!')

            # Redirect to the project main page
            return redirect('project:displayProject', project_id=project.id)
        else:
            # Message
            messages.warning(request, 'Some fields are not correct.')
    else:
        # Generate a form
        form = ModifyProjectForm()

    context = {
        'form': form,
        'project': project,
    }

    return render(request, 'project/modifyProject.html', context)


def delete_project_view(request, project_id):
    """
    Delete the project in the database.
    :param request:
    :param project_id:
    :return:
    """
    # Gather information
    project = Project.objects.get(id=project_id)

    # Modify content
    project.deletionDate = timezone.now()
    project.status = "Deleted"
    project.save()

    # Deletion
    project.delete()

    # Email contributor
    send_notifications_to_contributor(project)
    # Message
    messages.success(request, 'Project deleted')

    return redirect('project:index')


def team_members_listing_view(request, project_id):
    """
    Display members related to the project.
    :param request:
    :param project_id:
    :return:
    """
    # Gather information
    project = Project.objects.get(id=project_id)
    current_user_role = ContributorProject.objects.\
        get(project=project, projectPlannerUser=request.user)
    members = ContributorProject.objects.filter(project=project_id).\
        order_by('-permission')
    contributor_list = []
    for member in members:
        contributor_list.append(member.projectPlannerUser.email)

    # On POST method
    if request.method == 'POST':
        # Gather information from form
        form = AddMemberToProjectForm(request.POST)
        # Check that user designed is not already a contributor
        member_designed = ProjectPlannerUser.objects.\
            get(id=form.data['projectPlannerUser'])
        already_in_the_list_check = contributor_is_not_already_in_the_list(
            member_designed,
            contributor_list)

        if form.is_valid() and not already_in_the_list_check:
            # Add user in the project
            member_designed = ProjectPlannerUser.objects.\
                get(id=form.data['projectPlannerUser'])
            member_added = ContributorProject(project=project,
                                              projectPlannerUser=member_designed,
                                              permission='Contributor')
            member_added.save()

            # Message
            messages.success(request, 'A new team member is added!')

            # Reload page
            return redirect('project:teamMembersListing',
                            project_id=project_id)
        else:
            # Message
            messages.error(request, "User already in the team")

            # Reset field
            form = AddMemberToProjectForm()
    # Initial page call
    else:
        # Add a member
        form = AddMemberToProjectForm()

    # Generate a context
    context = {
        'project': project,
        'members': members,
        'form': form,
        'user_role': current_user_role.permission
    }

    return render(request, 'project/teamMembersListing.html', context)


def delete_team_member_view(request, member_id):
    """
    Remove a team member from a project.
    :param member_id:
    :return:
    """
    # Gather project information
    member_to_remove = ContributorProject.objects.get(id=member_id)
    project_id = member_to_remove.project.id

    # Remove member from contributor list
    member_to_remove.removingDate = timezone.now()
    member_to_remove.save()
    member_to_remove.delete()

    # Message
    messages.success(request, 'Team member removed')

    # Go back to homepage
    return redirect('project:teamMembersListing', project_id=project_id)


def deliverable_listing_view(request, project_id):
    """
    Display deliverables related to the project.
    :param request:
    :param project_id:
    :return:
    """
    # Gather project information
    project = Project.objects.get(id=project_id)
    current_user_role = ContributorProject.objects.\
        get(project=project, projectPlannerUser=request.user)
    deliverables = Deliverable.objects.\
        filter(project=project_id).order_by('dueDate')

    # On POST method
    if request.method == 'POST':
        # Gather information from form
        form = AddDeliverableToProjectForm(request.POST)
        if form.is_valid():
            # Generate a deliverable and modify content
            member_designed = ProjectPlannerUser.objects.\
                get(email=request.user.email)
            deliverable_added = Deliverable(name=form.data['name'],
                                            description=form.data['description'],
                                            dueDate=form.data['dueDate'],
                                            project=project)
            deliverable_added.save()
            contributor_deliverable = ContributorDeliverable(
                projectPlannerUser=member_designed,
                deliverable=deliverable_added)
            contributor_deliverable.save()

            # Reset field
            form = AddDeliverableToProjectForm()

            # Message
            messages.success(request, 'Deliverable added')
        else:
            # Message
            messages.error(request, 'Some fields are not correct.')

    # Initial page call
    else:
        # Add a deliverable
        form = AddDeliverableToProjectForm()

    # Generate a context
    context = {
        'project': project,
        'deliverables': deliverables,
        'form': form,
        'user_role': current_user_role.permission
    }

    return render(request, 'project/deliverablesListing.html', context)


def delete_deliverable_view(request, deliverable_id):
    """
    Remove a deliverable from a project.
    :param request:
    :param deliverable_id: deliverable id in the table
    :return:
    """
    # Gather information
    deliverable_to_remove = Deliverable.objects.get(id=deliverable_id)
    project_id = deliverable_to_remove.project.id

    # Modify content
    deliverable_to_remove.status = "Deleted"

    # Email contributor
    send_notifications_to_contributor(deliverable_to_remove)

    # Remove member from contributor list
    deliverable_to_remove.delete()

    # Message
    messages.success(request, 'Deliverable deleted')

    # Go back to homepage
    return redirect('project:deliverableListing', project_id=project_id)


def check_and_release_project_view(request, project_id):
    """
    Check if all deliverable are approved and modify the project status
    accordingly.
    :param request:
    :param project_id: id of the project
    :return:
    """
    # Gather information
    project = Project.objects.get(id=project_id)

    # Check the advancement of the project
    advancement = define_project_advancement(project_id)

    # If all deliverable finalized
    if advancement >= 100:
        project.status = "FINISHED"
        project.closureDate = timezone.now()
        project.save()

        # Email contributor
        send_notifications_to_contributor(project)
        # Message
        messages.success(request, 'Project finalized!')
    else:
        project.status = 'ON GOING'
        project.save()

        # Message
        messages.warning(request, 'Some deliverables are not finalized')

    # Go back to project home page
    return redirect("project:displayProject", project_id=project_id)


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
                      'project/displayDeliverable.html', context)
    else:
        # Frozen template - without form
        return render(request,
                      'project/displayDeliverableWithoutForms.html',
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
            return redirect('project:displayDeliverable',
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

    return render(request, 'project/modifyDeliverable.html', context)


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
        already_in_the_list_check = contributor_is_not_already_in_the_list(
            member_designed,
            contributor_list
        )

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
    return redirect('project:displayDeliverable',
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
    return redirect('project:displayDeliverable',
                    deliverable_id=deliverable_id)


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
        # Alert message
        messages.success(request,
                         "Feedback updated for : " + str(contributor.feedback))
    else:
        # Message
        messages.warning(request, 'Some fields are not correct!')

    # Redirect to homepage
    return redirect('project:displayDeliverable',
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

    # API config
    cloudinary.config(
        cloud_name=env.str('CLOUDINARY_CONFIG_CLOUD_NAME'),
        api_key=env.str('CLOUDINARY_CONFIG_API_KEY'),
        api_secret=env.str('CLOUDINARY_CONFIG_API_SECRET'),
        secure=True
    )

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

    return redirect("project:displayDeliverable",
                    deliverable_id=deliverable_id)
