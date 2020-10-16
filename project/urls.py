from django.conf.urls import url

from . import views
# import views so we can use them in urls.py.

app_name = 'project'

urlpatterns = [
    url(r'^$', views.index_view, name="index"),
    url(r'^mentions/$', views.mentions_view, name="mentions"),

    url(r'^createProject/$', views.create_project_view, name="createProject"),
    url(r'displayProject/(?P<project_id>[0-9]+)/$',
        views.display_project_view, name="displayProject"),
    url(r'^modifyProject/(?P<project_id>[0-9]+)/$',
        views.modify_project_view, name="modifyProject"),
    url(r'^deleteProject/(?P<project_id>[0-9]+)/$',
        views.delete_project_view, name="deleteProject"),

    url(r'^teamMembersListing/(?P<project_id>[0-9]+)/$',
        views.team_members_listing_view, name="teamMembersListing"),
    url(r'^deleteTeamMember/(?P<member_id>[0-9]+)/$',
        views.delete_team_member_view, name="DeleteTeamMember"),

    url(r'^deliverableListing/(?P<project_id>[0-9]+)/$',
        views.deliverable_listing_view, name="deliverableListing"),
    url(r'^deleteDeliverable/(?P<deliverable_id>[0-9]+)/$',
        views.delete_deliverable_view, name="DeleteDeliverable"),

    url(r'^checkAndReleaseProject/(?P<project_id>[0-9]+)/$',
        views.check_and_release_project_view, name="checkAndReleaseProject"),

    url(r'^displayDeliverable/(?P<deliverable_id>[0-9]+)/$',
        views.display_deliverable_view, name="displayDeliverable"),
    url(r'^modifyDeliverable/(?P<deliverable_id>[0-9]+)/$',
        views.modify_deliverable_view, name="modifyDeliverable"),

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
