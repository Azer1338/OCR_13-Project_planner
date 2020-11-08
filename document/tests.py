import unittest
import datetime
from unittest import mock
from unittest.mock import patch

from django.test import TestCase, Client


# display_deliverable_view Page
from accounts.models import ProjectPlannerUser
from document import models
from document.models import Document
from project.function_for_project import define_deliverable_progression
from project.models import Project, Deliverable, ContributorDeliverable


# add_document_to_deliverable_view Page
class AddDocumentToDeliverableViewTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate user
        test_user = ProjectPlannerUser.objects. \
            create_user(email="test_man@itest.com",
                        first_name="Claude",
                        name="Francois",
                        team="Designer",
                        password="Chanson",
                        )
        test_user.save()
        # Generate project
        project = Project.objects.create(name="TEST ADD DOCUMENT PROJECT")
        project.contributor.add(test_user)
        project.save()
        # Generate deliverable
        deliverable = Deliverable.objects. \
            create(name="TEST ADD DOCUMENT DELIVERABLE",
                   description="TEST ADD DOCUMENT DELIVERABLE DESCRIPTION",
                   project=project, )
        deliverable.contributor.add(test_user)
        deliverable.save()

        # Generate document
        with mock.patch('document.models.CloudinaryField', return_value='https//:www.all_ok.com'):
            document = Document.objects.create(name="TEST ADD DOCUMENT DOCUMENT",
                                               link="TEST LINK", deliverable=deliverable)
        document.save()

    def test_adding_a_document_to_deliverable_page_on_get_method(self):
        """Check a modification on model request by user.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Generate a dynamic url
        deliverable = Deliverable.objects.\
            get(name="TEST ADD DOCUMENT DELIVERABLE")
        url = '/document/addDocumentToDeliverable/' + \
              str(deliverable.id) + '/'
        response = c.get(url)

        # Check the return message
        self.assertEqual(response.status_code, 200)
        # Check context content
        self.assertEqual(str(response.context['deliverable'].name),
                         'TEST ADD DOCUMENT DELIVERABLE')
        self.assertTemplateUsed(response,
                                'document/addDocumentToDeliverable.html')

    @mock.patch('document.views.AddDocumentToDeliverableForm')
    def test_adding_a_document_to_deliverable_page_on_post_method(self, mock_check_output):
        """Check a modification on model request by user.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Generate a dynamic url
        deliverable = Deliverable.objects. \
            get(name="TEST ADD DOCUMENT DELIVERABLE")
        document = Document.objects.get(name='TEST ADD DOCUMENT DOCUMENT')
        url = '/document/addDocumentToDeliverable/' + \
              str(deliverable.id) + '/'
        response = c.post(url,
                          data={'deliverable': deliverable.id,
                                'name': 'Test',
                                'link': 'https//test.py'},
                          )
        # Generate a dynamic url
        url2 = '/displayDeliverable/' + str(deliverable.id) + '/'
        # Check the return message
        self.assertRedirects(response, url2, status_code=302)


# Deliverable model
class DeliverableTest(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate user
        test_user = ProjectPlannerUser.objects. \
            create_user(email="test_man@itest.com",
                        first_name="Claude",
                        name="Francois",
                        team="Designer",
                        password="Chanson",
                        )
        test_user.save()
        # Generate project
        project = Project.objects.create(name="TEST ADD CONTRIBUTOR PROJECT")
        project.contributor.add(test_user)
        project.save()
        # Generate deliverable
        deliverable = Deliverable.objects. \
            create(name="TEST ADD CONTRIBUTOR DELIVERABLE",
                   description="TEST ADD CONTRIBUTOR DELIVERABLE DESCRIPTION",
                   project=project, )
        deliverable.contributor.add(test_user)
        deliverable.save()
        # Generate document
        document = Document.objects. \
            create(name="TEST ADD CONTRIBUTOR DOCUMENT", link="TEST LINK",
                   deliverable=deliverable)
        document.save()

    def create_deliverable(self,
                           name="Livrable #1",
                           description="Description Livrable #1",
                           adding_date='2020-7-20',
                           due_date='2020-7-21',
                           closure_date='2020-7-22',
                           deletion_date='2020-7-23',
                           status="NEW",
                           progression=2,
                           ):
        # Gather information in database
        project = Project.objects.get(name="TEST ADD CONTRIBUTOR PROJECT")
        user = ProjectPlannerUser.objects.get(name="Francois")

        # Create a deliverable
        deliverable_test = Deliverable.objects. \
            create(name=name,
                   description=description,
                   addingDate=adding_date,
                   dueDate=due_date,
                   closureDate=closure_date,
                   deletionDate=deletion_date,
                   status=status,
                   progression=progression,
                   project=project,
                   )
        deliverable_test.contributor.add(user)

        return deliverable_test

    def test_deliverable_creation(self):
        deliverable = self.create_deliverable()
        self.assertTrue(isinstance(deliverable, Deliverable))


# Document model
class DocumentTest(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate user
        test_user = ProjectPlannerUser.objects. \
            create_user(email="test_man@itest.com",
                        first_name="Claude",
                        name="Francois",
                        team="Designer",
                        password="Chanson",
                        )
        test_user.save()
        # Generate project
        project = Project.objects.create(name="TEST ADD CONTRIBUTOR PROJECT")
        project.contributor.add(test_user)
        project.save()
        # Generate deliverable
        deliverable = Deliverable.objects. \
            create(name="TEST ADD CONTRIBUTOR DELIVERABLE",
                   description="TEST ADD CONTRIBUTOR DELIVERABLE DESCRIPTION",
                   project=project, )
        deliverable.contributor.add(test_user)
        deliverable.save()
        # Generate document
        document = Document.objects. \
            create(name="TEST ADD CONTRIBUTOR DOCUMENT", link="TEST LINK",
                   deliverable=deliverable)
        document.save()

    def create_document(self,
                        name="Document #1",
                        loading_date='2020-7-20',
                        link='https://test.py',
                        ):
        # Gather information in database
        deliverable = Deliverable.objects. \
            get(name="TEST ADD CONTRIBUTOR DELIVERABLE")

        # Create a deliverable
        deliverable_test = Document.objects. \
            create(name=name,
                   loadingDate=loading_date,
                   link=link,
                   deliverable=deliverable
                   )

        return deliverable_test

    def test_deliverable_creation(self):
        document = self.create_document()
        self.assertTrue(isinstance(document, Document))


# ContributorDeliverable model
class ContributorDeliverableTest(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate user
        test_user = ProjectPlannerUser.objects. \
            create_user(email="test_man@itest.com",
                        first_name="Claude",
                        name="Francois",
                        team="Designer",
                        password="Chanson",
                        )
        test_user.save()
        # Generate project
        project = Project.objects.create(name="TEST ADD CONTRIBUTOR PROJECT")
        project.contributor.add(test_user)
        project.save()
        # Generate deliverable
        deliverable = Deliverable.objects. \
            create(name="TEST ADD CONTRIBUTOR DELIVERABLE",
                   description="TEST ADD CONTRIBUTOR DELIVERABLE DESCRIPTION",
                   project=project, )
        deliverable.contributor.add(test_user)
        deliverable.save()
        # Generate document
        document = Document.objects. \
            create(name="TEST ADD CONTRIBUTOR DOCUMENT", link="TEST LINK",
                   deliverable=deliverable)
        document.save()

    def create_contributor(self,
                           function='CREATOR',
                           feedback='AGREED',
                           comment='I do not known what to say.',
                           ):
        # Gather information in database
        deliverable = Deliverable.objects. \
            get(name="TEST ADD CONTRIBUTOR DELIVERABLE")
        user = ProjectPlannerUser.objects. \
            get(first_name="Claude")

        # Create a deliverable
        contributor_test = ContributorDeliverable.objects. \
            create(function=function,
                   feedback=feedback,
                   comment=comment,
                   deliverable=deliverable,
                   projectPlannerUser=user
                   )

        return contributor_test

    def test_deliverable_creation(self):
        contributor = self.create_contributor()
        self.assertTrue(isinstance(contributor,
                                   ContributorDeliverable))


# Function for deliverable
class FunctionForDeliverableTest(unittest.TestCase):

    def test_define_deliverable_progression(self):
        # Creation of users
        test_user1 = ProjectPlannerUser.objects. \
            create(email="test_man4@itest.com",
                   first_name="Claude",
                   name="Francois",
                   team="Designer",
                   password="Chanson",
                   )
        test_user1.save()
        test_user2 = ProjectPlannerUser.objects. \
            create(email="test_man24@itest.com",
                   first_name="Claude",
                   name="Francois",
                   team="Designer",
                   password="Chanson",
                   )
        test_user2.save()

        # Creation of an project
        test_project = Project.objects.create(name="Test Project 3")
        test_project.save()
        test_project.contributor.add(test_user1)
        test_project.contributor.add(test_user2)
        test_project.save()

        # Creation of deliverables
        test_deliverable = Deliverable.objects. \
            create(name="Test Deliverable 3",
                   project=test_project)
        test_deliverable.save()
        test_deliverable.contributor.add(test_user1)
        test_deliverable.contributor.add(test_user2)
        test_deliverable.save()
        # Test user 2 is ok with deliverable
        contributor = ContributorDeliverable.objects.\
            get(projectPlannerUser=test_user1)
        contributor.feedback = "AGREED"
        contributor.save()

        progression = define_deliverable_progression(test_deliverable.id)
        self.assertEqual(progression, 50)
