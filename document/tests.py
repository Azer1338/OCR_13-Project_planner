import unittest
import datetime

from django.test import TestCase, Client


# display_deliverable_view Page
from accounts.models import ProjectPlannerUser
from document.models import Document
from project.function_for_project import define_deliverable_progression
from project.models import Project, Deliverable, ContributorDeliverable


class DisplayDeliverableViewTestCase(TestCase):

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
        # Generate another user
        test_user2 = ProjectPlannerUser.objects. \
            create_user(email="test_another_man@itest.com",
                        first_name="Coralie",
                        name="Bernard",
                        team="Accountant",
                        password="PouetPouet",
                        )
        test_user2.save()
        # Generate project
        project = Project.objects. \
            create(name="TEST DISPLAY PROJECT")
        project.contributor.add(test_user)
        project.save()
        # Generate deliverable
        deliverable = Deliverable.objects. \
            create(name="TEST DISPLAY DELIVERABLE",
                   description="TEST DELIVERABLE DESCRIPTION",
                   project=project,
                   )
        deliverable.contributor.add(test_user)
        deliverable.save()
        deliverable2 = Deliverable.objects. \
            create(name="TEST DISPLAY DELIVERABLE2",
                   description="TEST DELIVERABLE DESCRIPTION",
                   project=project,
                   )
        deliverable2.contributor.add(test_user)
        deliverable2.save()
        # Generate document - MOCK IT
        # image_linked_to_document = CloudinaryField('image',
        #                                            width_field="image_width",
        #                                            height_field="image_height",
        #                                            unique_filename='true',
        #                                            use_filename='true',
        #                                            phash='true',
        #                                            link='https/image.org/')
        # document = Document.objects.
        # create(name="TEST DISPLAY DOCUMENT", link=image_linked_to_document,
        # deliverable=deliverable)
        # document.save()

    def test_display_deliverable_page(self):
        """
        Check the right display of an existing deliverable.
        :return:
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Generate a dynamic url
        deliverable = Deliverable.objects.get(name="TEST DISPLAY DELIVERABLE")
        url = '/deliverable/displayDeliverable/' + str(deliverable.id) + '/'
        response = c.get(url)
        # Check the return message
        self.assertEqual(response.status_code, 200)
        # Check context content
        self.assertEqual(str(response.context['deliverable'].name),
                         'TEST DISPLAY DELIVERABLE')
        # self.assertEqual(str(response.context['documents'][0]),
        # 'TEST DISPLAY DOCUMENT')
        self.assertEqual(str(response.context['contributors'][0]),
                         'test_man@itest.com')
        self.assertTemplateUsed(response,
                                'deliverable/displayDeliverable.html')

    def test_display_a_frozen_deliverable_page(self):
        """
        Check the right display of an frozen deliverable.
        :return:
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com",
                password="Chanson")
        # Generate a dynamic url
        deliverable2 = Deliverable.objects. \
            get(name="TEST DISPLAY DELIVERABLE2")
        deliverable2.status = "APPROVED"
        deliverable2.save()
        url = '/deliverable/displayDeliverable/' + \
              str(deliverable2.id) + '/'
        response = c.get(url)

        # Check the return message
        self.assertEqual(response.status_code, 200)
        # Check context content
        self.assertEqual(str(response.context['deliverable'].name),
                         'TEST DISPLAY DELIVERABLE2')
        # self.assertEqual(str(response.context['documents'][0]),
        # 'TEST DISPLAY DOCUMENT')
        self.assertEqual(str(response.context['contributors'][0]),
                         'test_man@itest.com')
        self.assertTemplateUsed(response,
                                'deliverable/displayDeliverableWithoutForms.html')

    def test_display_a_deliverable_page_call_by_a_not_contributor(self):
        """Check the display deliverable page call by a not contributor.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_another_man@itest.com",
                password="PouetPouet")
        # Generate an url call
        deliverable_created = Deliverable.objects. \
            get(name="TEST DISPLAY DELIVERABLE2")
        url = '/deliverable/displayDeliverable/' + \
              str(deliverable_created.id) + '/'
        response = c.get(url,
                         data={'deliverable_id': deliverable_created.id
                               }
                         )
        # Check the return message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_user'], 'John DOE')


#  modify_deliverable_view Page
class ModifyDeliverableViewTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate user
        test_user1 = ProjectPlannerUser.objects. \
            create_user(email="test_man@itest.com",
                        first_name="Claude",
                        name="Francois",
                        team="Designer",
                        password="Chanson",
                        )
        test_user1.save()
        # Generate project
        project1 = Project.objects.create(name="TEST MODIFY PROJECT")
        project1.contributor.add(test_user1)
        project1.save()
        # Generate deliverable
        deliverable1 = Deliverable.objects. \
            create(name="TEST MODIFY DELIVERABLE",
                   description="TEST DELIVERABLE DESCRIPTION",
                   project=project1, )
        deliverable1.contributor.add(test_user1)
        deliverable1.save()
        # Generate document
        # document1 = Document.objects.
        # create(name="TEST MODIFY DOCUMENT",
        # link="TEST LINK", deliverable=deliverable1)
        # document1.save()

    def test_modify_deliverable_page(self):
        """Check a modification on model request by user.
        """
        # Generate a fake user
        c = Client()
        # Generate a dynamic url
        deliverable = Deliverable.objects. \
            get(name="TEST MODIFY DELIVERABLE")
        url = '/deliverable/modifyDeliverable/' + \
              str(deliverable.id) + '/'
        response = c.get(url)
        # Check the return message
        self.assertEqual(response.status_code, 200)

    def test_modify_a_deliverable_page_call_on_get_method(self):
        """Check the modification of a deliverable on get method.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Gather information
        deliverable = Deliverable.objects.get(name="TEST MODIFY DELIVERABLE")

        # Generate an dynamic url
        url = '/deliverable/modifyDeliverable/' + str(deliverable.id) + '/'
        response = c.get(url)

        # Check the return message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'deliverable/modifyDeliverable.html')

    def test_modify_a_deliverable_page_call_on_post_method(self):
        """Check the modification of a deliverable on post method.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Gather information
        deliverable = Deliverable.objects.get(name="TEST MODIFY DELIVERABLE")
        # Generate an dynamic url
        url = '/deliverable/modifyDeliverable/' + str(deliverable.id) + '/'
        response = c.post(url,
                          data={'description': 'Description modified',
                                'dueDate': '2000-11-10'
                                }
                          )
        # Load again
        deliverable = Deliverable.objects.get(name="TEST MODIFY DELIVERABLE")
        url2 = '/deliverable/displayDeliverable/' + str(deliverable.id) + '/'

        # Check the return message
        self.assertRedirects(response, url2, status_code=302)
        self.assertEqual(deliverable.description, 'Description modified')
        self.assertEqual(deliverable.dueDate, datetime.date(2000, 11, 10))


#  add_contributor_to_deliverable_view Page
class AddContributorToDeliverableViewTestCase(TestCase):

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
        test_user2 = ProjectPlannerUser.objects. \
            create_user(email="test_man2@itest.com",
                        first_name="Michel",
                        name="Berger",
                        team="Marketing",
                        password="Poussette",
                        )
        test_user2.save()
        # Generate project
        project = Project.objects. \
            create(name="TEST ADD CONTRIBUTOR PROJECT")
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
        # document = Document.objects.
        # create(name="TEST ADD CONTRIBUTOR DOCUMENT",
        # link="TEST LINK", deliverable=deliverable)
        # document.save()

    def test_adding_a_contributor_to_deliverable_page_on_get_method(self):
        """Check a modification on model request by user.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Generate a dynamic url
        deliverable = Deliverable.objects.\
            get(name="TEST ADD CONTRIBUTOR DELIVERABLE")
        url = '/deliverable/addContributorToDeliverable/' + \
              str(deliverable.id) + '/'
        response = c.get(url)
        url2 = '/deliverable/displayDeliverable/' + str(deliverable.id) + '/'
        # Check the return message
        self.assertRedirects(response, url2, status_code=302)

    def test_adding_a_contributor_to_deliverable_page_on_post_method(self):
        """Check a modification on model request by user.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Generate a dynamic url
        deliverable = Deliverable.objects. \
            get(name="TEST ADD CONTRIBUTOR DELIVERABLE")
        user = ProjectPlannerUser.objects.get(name="Berger")
        url = '/deliverable/addContributorToDeliverable/' + \
              str(deliverable.id) + '/'
        response = c.post(url,
                          data={'projectPlannerUser': user.id,
                                'function': 'COLLABORATOR'
                                }
                          )
        contributor_list = ContributorDeliverable.objects. \
            filter(deliverable=deliverable)
        # Generate a dynamic url
        url2 = '/deliverable/displayDeliverable/' + str(deliverable.id) + '/'

        # Check the return message
        self.assertRedirects(response, url2, status_code=302)
        self.assertEqual(len(contributor_list), 2)
        self.assertEqual(str(contributor_list[0]), str(user))


# remove_contributor_from_deliverable_view Page
class RemoveContributorFromDeliverableVTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate users
        test_user = ProjectPlannerUser.objects. \
            create_user(email="test_man@itest.com",
                        first_name="Claude",
                        name="Francois",
                        team="Designer",
                        password="Chanson",
                        )
        test_user.save()
        test_user2 = ProjectPlannerUser.objects. \
            create_user(email="test_man2@itest.com",
                        first_name="Michel",
                        name="Berger",
                        team="Marketing",
                        password="Poussette",
                        )
        test_user2.save()
        # Generate project
        project = Project.objects.create(name="TEST TEAM LISTING PROJECT")
        project.contributor.add(test_user)
        project.contributor.add(test_user2)
        project.save()
        # Generate deliverable
        deliverable = Deliverable.objects. \
            create(name="TEST TEAM LISTING DELIVERABLE",
                   description="TEST TEAM LISTING DELIVERABLE DESCRIPTION",
                   project=project, )
        deliverable.contributor.add(test_user)
        deliverable.contributor.add(test_user2)
        deliverable.save()
        # Generate document
        # document = Document.objects.
        # create(name="TEST TEAM LISTING DOCUMENT",
        # link="TEST LINK", deliverable=deliverable)
        # document.save()

    def test_remove_contributor_deliverable(self):
        """Check the removing team member call.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Gather info
        deliverable = Deliverable.objects. \
            get(name="TEST TEAM LISTING DELIVERABLE")
        contributor_initial_list_length = len(ContributorDeliverable.
                                              objects.filter(deliverable=deliverable))
        user2 = ProjectPlannerUser.objects.get(name='Berger')
        contributor_to_remove = ContributorDeliverable.objects \
            .get(projectPlannerUser=user2)

        # Generate an url call
        url = '/deliverable/removeContributorFromDeliverable/' + \
              str(contributor_to_remove.id) + '/'
        response = c.get(url)
        # Reload
        deliverable = Deliverable.objects. \
            get(name="TEST TEAM LISTING DELIVERABLE")
        contributor_final_list_length = len(ContributorDeliverable.objects.
                                            filter(deliverable=deliverable))

        # Check the return message
        url2 = '/deliverable/displayDeliverable/' + str(deliverable.id) + '/'
        self.assertRedirects(response, url2, status_code=302)
        self.assertNotEqual(contributor_initial_list_length,
                            contributor_final_list_length)


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
        # document = Document.objects.
        # create(name="TEST ADD DOCUMENT DOCUMENT",
        # link="TEST LINK", deliverable=deliverable)
        # document.save()

    def test_adding_a_document_to_deliverable_page_on_get_method(self):
        """Check a modification on model request by user.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Generate a dynamic url
        deliverable = Deliverable.objects.\
            get(name="TEST ADD DOCUMENT DELIVERABLE")
        url = '/deliverable/addDocumentToDeliverable/' + \
              str(deliverable.id) + '/'
        response = c.get(url)

        # Check the return message
        self.assertEqual(response.status_code, 200)
        # Check context content
        self.assertEqual(str(response.context['deliverable'].name),
                         'TEST ADD DOCUMENT DELIVERABLE')
        self.assertTemplateUsed(response,
                                'deliverable/addDocumentToDeliverable.html')

    def test_adding_a_document_to_deliverable_page_on_post_method(self):
        """Check a modification on model request by user.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Generate a dynamic url
        deliverable = Deliverable.objects. \
            get(name="TEST ADD DOCUMENT DELIVERABLE")
        url = '/deliverable/addDocumentToDeliverable/' + \
              str(deliverable.id) + '/'
        response = c.post(url,
                          data={'deliverable': deliverable.id,
                                'name': 'Test',
                                'kindOf': 'EXCEL',
                                'link': 'https//test.py'},
                          )
        # Generate a dynamic url
        url2 = '/deliverable/displayDeliverable/' + str(deliverable.id) + '/'
        # Check the return message
        self.assertRedirects(response, url2, status_code=302)


# update_contribution_feedback_to_deliverable_view Page
class UpdateContributionFeedbackToDeliverableViewTestCase(TestCase):

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
        # document = Document.objects.
        # create(name="TEST ADD DOCUMENT DOCUMENT", link="TEST LINK",
        # deliverable=deliverable)
        # document.save()

    def test_update_contribution_feedback_to_deliverable_on_get_method(self):
        """Check a modification on comment/feedback request by
         user on get method.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Gather information
        deliverable = Deliverable.objects. \
            get(name="TEST ADD DOCUMENT DELIVERABLE")
        user = ProjectPlannerUser.objects.get(name='Francois')
        contributor = ContributorDeliverable.objects. \
            get(projectPlannerUser=user, deliverable=deliverable)

        # Get to the url
        url = '/deliverable/updateContributionToDeliverable/' + \
              str(contributor.id) + '/'
        response = c.get(url)

        # Generate a dynamic url
        url2 = '/deliverable/displayDeliverable/' + str(deliverable.id) + '/'

        # Check the return message
        self.assertRedirects(response, url2, status_code=302)

    def test_update_contribution_feedback_to_deliverable_on_post_method(self):
        """Check a modification on comment/feedback request by user
        on post method.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Gather information
        deliverable = Deliverable.objects. \
            get(name="TEST ADD DOCUMENT DELIVERABLE")
        user = ProjectPlannerUser.objects.get(name='Francois')
        contributor = ContributorDeliverable.objects. \
            get(projectPlannerUser=user, deliverable=deliverable)

        # Generate a dynamic url
        url = '/deliverable/updateContributionToDeliverable/' + \
              str(contributor.id) + '/'
        response = c.post(url,
                          data={'feedback': 'AGREED',
                                'comment': 'This is a updated comment'
                                },
                          )
        # Load again
        contributor = ContributorDeliverable.objects. \
            get(projectPlannerUser=user, deliverable=deliverable)

        # Generate a dynamic url
        url2 = '/deliverable/displayDeliverable/' + str(deliverable.id) + '/'
        # Check the return message
        self.assertRedirects(response, url2, status_code=302)
        self.assertEqual(contributor.comment, 'This is a updated comment')


# check_and_release_deliverable_view Page
class CheckAndReleaseDeliverableViewTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate users
        test_user = ProjectPlannerUser.objects. \
            create_user(email="test_man@itest.com",
                        first_name="Claude",
                        name="Francois",
                        team="Designer",
                        password="Chanson",
                        )
        test_user.save()
        test_user2 = ProjectPlannerUser.objects. \
            create_user(email="test_man2@itest.com",
                        first_name="Michel",
                        name="Berger",
                        team="Marketing",
                        password="Poussette",
                        )
        test_user2.save()
        # Generate project
        project = Project.objects.create(name="TEST CHECK N RELEASE PROJECT")
        project.contributor.add(test_user)
        project.save()
        # Generate deliverable
        deliverable = Deliverable.objects. \
            create(name="TEST CHECK N RELEASE DELIVERABLE",
                   description="TEST DELIVERABLE LISTING DELIVERABLE DESCRIPTION",
                   project=project, )
        deliverable.contributor.add(test_user)
        deliverable.save()
        # Generate document
        document = Document.objects. \
            create(name="TEST DELIVERABLE LISTING DOCUMENT", link="TEST LINK",
                   deliverable=deliverable)
        document.save()

    def test_check_and_release_project_view_page(self):
        """Check the check and release a project.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Gather information
        deliverable = Deliverable.objects. \
            get(name="TEST CHECK N RELEASE DELIVERABLE")
        user = ProjectPlannerUser.objects.get(name='Francois')
        # Force contributor to agreed on deliverable
        contributor = ContributorDeliverable.objects. \
            get(projectPlannerUser=user, deliverable=deliverable)
        contributor.feedback = 'AGREED'
        contributor.save()
        # Generate an url call
        url = '/deliverable/checkAndReleaseDeliverable/' + \
              str(deliverable.id) + '/'
        response = c.get(url)
        url2 = '/deliverable/displayDeliverable/' + str(deliverable.id) + '/'

        # Load again
        deliverable = Deliverable.objects. \
            get(name="TEST CHECK N RELEASE DELIVERABLE")

        # Check the return message
        self.assertRedirects(response, url2, status_code=302)
        self.assertEqual(deliverable.status, "APPROVED")


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
        contributor = ContributorDeliverable.objects.get(projectPlannerUser=test_user1)
        contributor.feedback = "AGREED"
        contributor.save()

        progression = define_deliverable_progression(test_deliverable.id)
        self.assertEqual(progression, 50)
