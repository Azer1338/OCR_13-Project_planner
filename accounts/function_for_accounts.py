# Some functions to support the code
from django.core.mail import EmailMessage
from django_mailgun import MailgunAPIError

from project.models import ContributorDeliverable, ContributorProject


def send_notifications_to_contributor(event_from):
    """
    Send an email to contributors with a specific message.
    :param event_from:
    :return:
    """
    # In case of Deliverable
    if str(type(event_from)) == "<class 'project.models.Deliverable'>":
        # Email title
        title_email = 'Event on your deliverable! - ' + \
                      event_from.project.name + ' - ' + \
                      event_from.name + ' - Project Planner'
        # Email body
        body_email = 'The deliverable ' + event_from.name + \
                     ' in the project ' + event_from.project.name + \
                     ', just move to ' + event_from.status + '.'
        contributor_list = ContributorDeliverable.objects.filter(deliverable=event_from.id)

    # In case of Project
    elif str(type(event_from)) == "<class 'project.models.Project'>":
        # Email title
        title_email = 'Event on your project ' + event_from.name + \
                      ' ! - Project Planner'
        # Email body
        body_email = 'The project ' + event_from.name + \
                     ', just move to ' + event_from.status + '.'
        contributor_list = ContributorProject.objects.filter(project=event_from.id)

    # Other event
    else:
        # Email title
        title_email = 'Undefined events on Project Planner'
        # Email body
        body_email = 'An event is detected'
        # Admin's email
        contributor_list = ['adrien13.f@gmail.com']

    # Gather contributor list
    contributor_email_list = []
    for contributor in contributor_list:
        contributor_email_list.append(str(contributor.projectPlannerUser.email))

    # Sending
    email = EmailMessage(title_email,
                         body_email,
                         'contact@projetplanner.org',
                         contributor_email_list,
                         )
    # Raise an Error if someone is not add into Mailgun interface.
    try:
        email.send()
        # Message
        message= "Successfully send!"
    except MailgunAPIError as error:
        # Message
        message = "Contributors is not log on Mailgun"
        print("Contributors is not log on Mailgun. " + str(error))

    return message


