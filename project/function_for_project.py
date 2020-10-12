# Some functions to support the apps
from deliverable.models import Deliverable, ContributorDeliverable


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