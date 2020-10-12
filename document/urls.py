from django.conf.urls import url

from . import views


app_name = 'document'

urlpatterns = [
    url(r'^addDocumentToDeliverable/(?P<deliverable_id>[0-9]+)/$',
        views.add_document_to_deliverable_view,
        name="addDocumentToDeliverable"),
]
