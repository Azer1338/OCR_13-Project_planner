from django.conf.urls import url

from . import views


app_name = 'document'

urlpatterns = [
    url(r'^displayDeliverable/(?P<deliverable_id>[0-9]+)/$',
        views.display_deliverable_view, name="displayDeliverable"),
    url(r'^modifyDeliverable/(?P<deliverable_id>[0-9]+)/$',
        views.modify_deliverable_view, name="modifyDeliverable"),

    url(r'^addDocumentToDeliverable/(?P<deliverable_id>[0-9]+)/$',
        views.add_document_to_deliverable_view,
        name="addDocumentToDeliverable"),

    url(r'^addContributorToDeliverable/(?P<deliverable_id>[0-9]+)/$',
        views.add_contributor_to_deliverable_view,
        name="addContributorToDeliverable"),
    url(r'^removeContributorFromDeliverable/(?P<member_id>[0-9]+)/$',
        views.remove_contributor_from_deliverable_view,
        name="removeContributorFromDeliverable"),

    url(r'^updateContributionToDeliverable/(?P<contributor_id>[0-9]+)/$',
        views.update_contribution_feedback_to_deliverable_view,
        name="updateContributionToDeliverable"),

    url(r'^checkAndReleaseDeliverable/(?P<deliverable_id>[0-9]+)/$',
        views.check_and_release_deliverable_view,
        name="checkAndReleaseDeliverable"),
]