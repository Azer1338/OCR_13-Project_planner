# Some functions to support the apps
from deliverable.models import Deliverable, ContributorDeliverable
from deliverable.models import Deliverable
from project.models import Project

def define_deliverable_progression(deliverable_id):
    """
    Define the number of deliverable approved vs not approved.
    :param deliverable_id: id of the project
    :return:
    """
    # Gather information
    contributors = ContributorDeliverable.objects.\
        filter(deliverable=deliverable_id)
    deliverable = Deliverable.objects.get(id=deliverable_id)

    # Gather all contributors feedback
    contributors_feedback = []
    for contributor in contributors:
        contributors_feedback.append(contributor.feedback)
    # Init count
    agreement_count = contributors_feedback.count("AGREED")

    # Define the progression
    progression = int((agreement_count/len(contributors))*100)

    # Modify project status
    deliverable.progression = progression
    deliverable.save()

    return progression




def contributor_is_not_already_in_the_list(contributor, listing):
    """
    Return False if the contributor is already in the list.
    :param listing: list of contributor
    :param contributor: name of the contributor
    :return: False is the contributor is already in the list
    """
    # Format the input
    contributor = str(contributor)

    # Go through the list
    if contributor in listing:
        return True
    else:
        return False


def define_project_advancement(project_id):
    """
    Define the number of deliverable approved vs not approved.
    :param project_id: id of the project
    :return:
    """
    # Gather information
    deliverables = Deliverable.objects.filter(project=project_id)
    project = Project.objects.get(id=project_id)

    # Gather all deliverable status
    deliverables_status = []
    for deliverable in deliverables:
        deliverables_status.append(deliverable.status)
    # Init count
    agreement_count = deliverables_status.count("APPROVED")

    # Define the project advancement
    advancement = int((agreement_count/len(deliverables))*100)

    # Modify project status
    project.advancement = advancement
    project.save()

    return advancement