# Some functions to support the code
from django.core.mail import EmailMessage

from project.models import Deliverable, Project


def send_notifications_to_contributor(event_from):
    """
    Send an email to contributors with a specific message.
    :param event_from:
    :return:
    """
    # In case of Deliverable
    if str(type(event_from)) == "<class 'deliverable.models.Deliverable'>":
        # Email title
        title_email = 'Event on your deliverable! - ' + \
                      event_from.project.name + ' - ' + \
                      event_from.name + ' - Project Planner'
        # Email body
        body_email = 'The deliverable ' + event_from.name + \
                     ' in the project' + event_from.project.name + \
                     ', just move to ' + event_from.status + '.'
        contributor_list = Deliverable.objects.filter(name=event_from)

    # In case of Project
    elif str(type(event_from)) == "<class 'project.models.Project'>":
        # Email title
        title_email = 'Event on your project ' + event_from.name + \
                      ' ! - Project Planner'
        # Email body
        body_email = 'The project ' + event_from.name + \
                     ', just move to ' + event_from.status + '.'
        contributor_list = Project.objects.filter(name=event_from)

    # Other event
    else:
        # Email title
        title_email = 'Event on Project Planner'
        # Email body
        body_email = 'An event is detected'
        # Admin's email
        contributor_list = ['adrien13.f@gmail.com']

    # FOR TEST PURPOSE
    contributor_list = ['adrien13.f@gmail.com']

    # Sending
    email = EmailMessage(title_email,
                         body_email,
                         'contact@projetplanner.org',
                         contributor_list,
                         )
    email.send()
