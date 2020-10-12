import datetime

from django.test import TestCase, Client
from accounts import ProjectPlannerUser
from deliverable import Deliverable, Document, ContributorDeliverable
from project.function_for_project import contributor_is_not_already_in_the_list, define_project_advancement
from project.models import Project, ContributorProject


#  index_view Page#
class IndexViewTestCase(TestCase):

    def test_index_page_call(self):
        """Check the index page call.
        """
        # Generate a fake user
        c = Client()
        # Get a page
        response = c.get('/')
        # Check the return message
        self.assertEqual(response.status_code, 200)


#  mentions_view Page
class MentionsViewTestCase(TestCase):

    def test_mention_page_call(self):
        """Check the mentions page call.
        """
        # Generate a fake user
        c = Client()
        # Get a page
        response = c.get('/mentions/')
        # Check the return message
        self.assertEqual(response.status_code, 200)


#  create_project_view Page
class CreateProjectViewTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate user
        test_user = ProjectPlannerUser.objects.create_user(email="test_man@itest.com",
                                                           first_name="Claude",
                                                           name="Francois",
                                                           team="Designer",
                                                           password="Chanson",
                                                           )
        test_user.save()
        # Generate project
        project = Project.objects.create(name="TEST CREATE PROJECT PROJECT")
        project.contributor.add(test_user)
        project.save()
        # Generate deliverable
        deliverable = Deliverable.objects.create(name="TEST CREATE PROJECT DELIVERABLE",
                                                 description="TEST CREATE PROJECT DELIVERABLE DESCRIPTION",
                                                 project=project, )
        deliverable.contributor.add(test_user)
        deliverable.save()
        # Generate document
        document = Document.objects.create(name="TEST CREATE PROJECT DOCUMENT", link="TEST LINK",
                                           deliverable=deliverable)
        document.save()

    def test_create_a_project_page_on_get_method(self):
        """Check the create project page call.
        """
        # Generate a fake user
        c = Client()
        # Generate an url call
        response = c.get('/createProject/')
        # Check the return message
        self.assertEqual(response.status_code, 200)

    def test_create_a_project_page_on_post_method(self):
        """Check the creation of a project.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Generate an url
        response = c.post('/createProject/',
                          data={'name': 'Test - Create a project',
                                'description': 'Test',
                                }
                          )
        # Generate a dynamic url
        project_created = Project.objects.get(name='Test - Create a project')
        url2 = '/displayProject/' + str(project_created.id) + '/'
        # # Check the return message
        self.assertRedirects(response, url2, status_code=302)


#  display_project_view Page
class DisplayProjectViewTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate user
        test_user = ProjectPlannerUser.objects.create_user(email="test_man@itest.com",
                                                           first_name="Claude",
                                                           name="Francois",
                                                           team="Designer",
                                                           password="Chanson",
                                                           )
        test_user.save()
        # Generate another user
        test_user2 = ProjectPlannerUser.objects.create_user(email="test_another_man@itest.com",
                                                            first_name="Coralie",
                                                            name="Bernard",
                                                            team="Accountant",
                                                            password="PouetPouet",
                                                            )
        test_user2.save()
        # Generate project
        project = Project.objects.create(name="TEST DISPLAY PROJECT")
        project.contributor.add(test_user)
        project.save()
        # Generate deliverable
        deliverable = Deliverable.objects.create(name="TEST DISPLAY PROJECT DELIVERABLE",
                                                 description="TEST DISPLAY PROJECT DELIVERABLE DESCRIPTION",
                                                 project=project, )
        deliverable.contributor.add(test_user)
        deliverable.save()
        # Generate document
        document = Document.objects.create(name="TEST DISPLAY PROJECT DOCUMENT", link="TEST LINK",
                                           deliverable=deliverable)
        document.save()

    def test_display_a_project_page_call(self):
        """Check the display project page call.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Generate an url call
        project_created = Project.objects.get(name="TEST DISPLAY PROJECT")
        url2 = '/displayProject/' + str(project_created.id) + '/'
        response = c.get(url2,
                         data={'project_id': project_created.id
                               }
                         )
        # Check the return message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/displayProject.html')

    def test_display_a_project_page_call_by_a_not_contributor(self):
        """Check the display project page call by a not contributor.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_another_man@itest.com", password="PouetPouet")
        # Generate an url call
        project_created = Project.objects.get(name="TEST DISPLAY PROJECT")
        url2 = '/displayProject/' + str(project_created.id) + '/'
        response = c.get(url2,
                         data={'project_id': project_created.id
                               }
                         )
        # Check the return message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_user'], 'John DOE')

    def test_display_a_frozen_project_page_call(self):
        """Check the display of a frozen project page.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Generate an url call
        project_created = Project.objects.get(name="TEST DISPLAY PROJECT")
        project_created.status = "FINISHED"
        project_created.save()
        url2 = '/displayProject/' + str(project_created.id) + '/'
        response = c.get(url2,
                         data={'project_id': project_created.id
                               }
                         )
        # Check the return message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/displayProjectWithoutForms.html')


# modify_project_view Page
class ModifyProjectViewTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate user
        test_user = ProjectPlannerUser.objects.create_user(email="test_man@itest.com",
                                                           first_name="Claude",
                                                           name="Francois",
                                                           team="Designer",
                                                           password="Chanson",
                                                           )
        test_user.save()
        # Generate project
        project = Project.objects.create(name="TEST DISPLAY PROJECT",
                                         description="This is a initial description",
                                         dueDate='1990-11-10')
        project.contributor.add(test_user)
        project.save()
        # Generate deliverable
        deliverable = Deliverable.objects.create(name="TEST DISPLAY PROJECT DELIVERABLE",
                                                 description="TEST DISPLAY PROJECT DELIVERABLE DESCRIPTION",
                                                 project=project, )
        deliverable.contributor.add(test_user)
        deliverable.save()
        # Generate document
        document = Document.objects.create(name="TEST DISPLAY PROJECT DOCUMENT", link="TEST LINK",
                                           deliverable=deliverable)
        document.save()

    def test_modify_a_project_page_call_on_get_method(self):
        """Check the modification of a project on get method.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Gather information
        project = Project.objects.get(name="TEST DISPLAY PROJECT")

        # Generate an dynamic url
        url2 = '/modifyProject/' + str(project.id) + '/'
        response = c.get(url2)

        # Check the return message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/modifyProject.html')

    def test_modify_a_project_page_call_on_post_method(self):
        """Check the modification of a project on post method.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Gather information
        project = Project.objects.get(name="TEST DISPLAY PROJECT")

        # Generate an dynamic url
        url2 = '/modifyProject/' + str(project.id) + '/'
        response = c.post(url2,
                          data={'description': 'Description modified',
                                'dueDate': '2000-11-10'
                                }
                          )
        # Load again
        project = Project.objects.get(name="TEST DISPLAY PROJECT")
        # Check the return message
        self.assertEqual(response.status_code, 302)
        self.assertEqual(project.description, 'Description modified')
        self.assertEqual(project.dueDate, datetime.date(2000, 11, 10))


#  delete_project_view Page
class DeleteProjectViewTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate user
        test_user = ProjectPlannerUser.objects.create_user(email="test_man@itest.com",
                                                           first_name="Claude",
                                                           name="Francois",
                                                           team="Designer",
                                                           password="Chanson",
                                                           )
        test_user.save()
        # Generate project
        project = Project.objects.create(name="TEST DISPLAY PROJECT")
        project.contributor.add(test_user)
        project.save()
        # Generate deliverable
        deliverable = Deliverable.objects.create(name="TEST DISPLAY PROJECT DELIVERABLE",
                                                 description="TEST DISPLAY PROJECT DELIVERABLE DESCRIPTION",
                                                 project=project, )
        deliverable.contributor.add(test_user)
        deliverable.save()
        # Generate document
        document = Document.objects.create(name="TEST DISPLAY PROJECT DOCUMENT", link="TEST LINK",
                                           deliverable=deliverable)
        document.save()

    def test_delete_a_project_page_call(self):
        """Check the removing of project.
        """
        # Generate a fake user
        c = Client()
        # Generate an url call
        project_created = Project.objects.get(name="TEST DISPLAY PROJECT")
        url2 = '/deleteProject/' + str(project_created.id) + '/'
        response = c.get(url2,
                         data={'project_id': project_created.id
                               }
                         )
        # Load it again
        project_list = Project.objects.filter(name="TEST DISPLAY PROJECT")

        # Check the return message
        self.assertRedirects(response, '/', status_code=302)
        self.assertEqual(len(project_list), 0)


#  team_members_listing_view Page
class TeamMembersListingViewTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate users
        test_user = ProjectPlannerUser.objects.create_user(email="test_man@itest.com",
                                                           first_name="Claude",
                                                           name="Francois",
                                                           team="Designer",
                                                           password="Chanson",
                                                           )
        test_user.save()
        test_user2 = ProjectPlannerUser.objects.create_user(email="test_man2@itest.com",
                                                            first_name="Michel",
                                                            name="Berger",
                                                            team="Marketing",
                                                            password="Poussette",
                                                            )
        test_user2.save()
        # Generate project
        project = Project.objects.create(name="TEST TEAM LISTING PROJECT")
        project.contributor.add(test_user)
        project.save()
        # Generate deliverable
        deliverable = Deliverable.objects.create(name="TEST TEAM LISTING DELIVERABLE",
                                                 description="TEST TEAM LISTING DELIVERABLE DESCRIPTION",
                                                 project=project, )
        deliverable.contributor.add(test_user)
        deliverable.save()
        # Generate document
        document = Document.objects.create(name="TEST TEAM LISTING DOCUMENT", link="TEST LINK",
                                           deliverable=deliverable)
        document.save()

    def test_team_listing_page_on_get_method(self):
        """Check the team listing  page call.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Generate an url call
        project = Project.objects.get(name="TEST TEAM LISTING PROJECT")
        url = '/teamMembersListing/' + str(project.id) + '/'
        response = c.get(url)
        # Check the return message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/projectTeamMembersListing.html')

    def test_team_listing_page_on_post_method_new_contributor(self):
        """Check the adding of a new contributor on the project.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Generate a dynamic url
        project_created = Project.objects.get(name="TEST TEAM LISTING PROJECT")
        test_user2 = ProjectPlannerUser.objects.get(name="Berger")
        url = '/teamMembersListing/' + str(project_created.id) + '/'
        response = c.post(url,
                          data={'projectPlannerUser': test_user2.id,
                                }
                          )
        # Load it again
        project_created = Project.objects.get(name="TEST TEAM LISTING PROJECT")
        contributor_list = ProjectPlannerUser.objects.filter(project=project_created)

        # Check the return message
        url = '/teamMembersListing/' + str(project_created.id) + '/'
        self.assertRedirects(response, url, status_code=302)
        self.assertEqual(len(contributor_list), 2)
        self.assertEqual(str(contributor_list[0]), str(test_user2))

    def test_team_listing_page_on_post_method_already_contributor(self):
        """Check the adding of a already contributor on the project.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Generate a dynamic url
        project_created = Project.objects.get(name="TEST TEAM LISTING PROJECT")
        test_user = ProjectPlannerUser.objects.get(name="Francois")
        url = '/teamMembersListing/' + str(project_created.id) + '/'
        response = c.post(url,
                          data={'projectPlannerUser': test_user.id,
                                }
                          )
        # Load it again
        project_created = Project.objects.get(name="TEST TEAM LISTING PROJECT")
        contributor_list = ProjectPlannerUser.objects.filter(project=project_created)

        # Check the return message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(contributor_list), 1)


# delete_team_member_view Page
class DeleteTeamMemberViewTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate users
        test_user = ProjectPlannerUser.objects.create_user(email="test_man@itest.com",
                                                           first_name="Claude",
                                                           name="Francois",
                                                           team="Designer",
                                                           password="Chanson",
                                                           )
        test_user.save()
        test_user2 = ProjectPlannerUser.objects.create_user(email="test_man2@itest.com",
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
        deliverable = Deliverable.objects.create(name="TEST TEAM LISTING DELIVERABLE",
                                                 description="TEST TEAM LISTING DELIVERABLE DESCRIPTION",
                                                 project=project, )
        deliverable.contributor.add(test_user)
        deliverable.save()
        # Generate document
        document = Document.objects.create(name="TEST TEAM LISTING DOCUMENT", link="TEST LINK",
                                           deliverable=deliverable)
        document.save()

    def test_delete_team_member(self):
        """Check the removing team member call.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Gather info
        project = Project.objects.get(name="TEST TEAM LISTING PROJECT")
        contributor_initial_list_length = len(ContributorProject.objects.filter(project=project))
        user2 = ProjectPlannerUser.objects.get(name='Berger')
        contributor_to_remove = ContributorProject.objects.get(projectPlannerUser=user2)

        # Generate an url call
        url = '/deleteTeamMember/' + str(contributor_to_remove.id) + '/'
        response = c.get(url)
        # Reload
        project = Project.objects.get(name="TEST TEAM LISTING PROJECT")
        contributor_final_list_length = len(ContributorProject.objects.filter(project=project))

        # Check the return message
        url2 = '/teamMembersListing/' + str(project.id) + '/'
        self.assertRedirects(response, url2, status_code=302)
        self.assertNotEqual(contributor_initial_list_length, contributor_final_list_length)


# deliverable_listing_view Page
class DeliverablesListingViewTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate users
        test_user = ProjectPlannerUser.objects.create_user(email="test_man@itest.com",
                                                           first_name="Claude",
                                                           name="Francois",
                                                           team="Designer",
                                                           password="Chanson",
                                                           )
        test_user.save()
        test_user2 = ProjectPlannerUser.objects.create_user(email="test_man2@itest.com",
                                                            first_name="Michel",
                                                            name="Berger",
                                                            team="Marketing",
                                                            password="Poussette",
                                                            )
        test_user2.save()
        # Generate project
        project = Project.objects.create(name="TEST DELIVERABLE LISTING PROJECT")
        project.contributor.add(test_user)
        project.save()
        # Generate deliverable
        deliverable = Deliverable.objects.create(name="TEST DELIVERABLE LISTING DELIVERABLE",
                                                 description="TEST DELIVERABLE LISTING DELIVERABLE DESCRIPTION",
                                                 project=project, )
        deliverable.contributor.add(test_user)
        deliverable.save()
        # Generate document
        document = Document.objects.create(name="TEST DELIVERABLE LISTING DOCUMENT", link="TEST LINK",
                                           deliverable=deliverable)
        document.save()

    def test_deliverable_listing_page_on_get_method(self):
        """Check the team listing  page call on get method.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Generate an url call
        project = Project.objects.get(name="TEST DELIVERABLE LISTING PROJECT")
        url = '/deliverableListing/' + str(project.id) + '/'
        response = c.get(url)
        # Check the return message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/projectDeliverablesListing.html')

    def test_deliverable_listing_page_on_post_method(self):
        """Check the team listing  page call on post method.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Generate a dynamic url
        project_created = Project.objects.get(name="TEST DELIVERABLE LISTING PROJECT")
        test_user2 = ProjectPlannerUser.objects.get(name="Berger")
        url = '/deliverableListing/' + str(project_created.id) + '/'
        response = c.post(url,
                          data={'name': 'Test Deliverable name',
                                'description': 'This is the description',
                                'dueDate': '2000-11-10'
                                }
                          )
        # Looking for the deliverable
        deliverable_created = Deliverable.objects.get(name='Test Deliverable name')
        contributor = ContributorDeliverable.objects.filter(deliverable=deliverable_created)
        contributor = str(contributor[0])
        # Check the return message
        self.assertEqual(response.status_code, 200)
        self.assertTrue(deliverable_created)
        self.assertEqual(contributor, 'test_man@itest.com')


# delete_deliverable_view Page
class DeleteDeliverableViewTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate users
        test_user = ProjectPlannerUser.objects.create_user(email="test_man@itest.com",
                                                           first_name="Claude",
                                                           name="Francois",
                                                           team="Designer",
                                                           password="Chanson",
                                                           )
        test_user.save()
        test_user2 = ProjectPlannerUser.objects.create_user(email="test_man2@itest.com",
                                                            first_name="Michel",
                                                            name="Berger",
                                                            team="Marketing",
                                                            password="Poussette",
                                                            )
        test_user2.save()
        # Generate project
        project = Project.objects.create(name="TEST DELETE DELIVERABLE")
        project.contributor.add(test_user)
        project.save()
        # Generate deliverable
        deliverable = Deliverable.objects.create(name="TEST DELETE DELIVERABLE",
                                                 description="TEST DELIVERABLE LISTING DELIVERABLE DESCRIPTION",
                                                 project=project, )
        deliverable.contributor.add(test_user)
        deliverable.save()
        # Generate document
        document = Document.objects.create(name="TEST DELIVERABLE LISTING DOCUMENT", link="TEST LINK",
                                           deliverable=deliverable)
        document.save()

    def test_delete_deliverable_page(self):
        """Check the removing of a deliverable.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Generate an url call
        deliverable = Deliverable.objects.get(name="TEST DELETE DELIVERABLE")
        url = '/deleteDeliverable/' + str(deliverable.id) + '/'
        response = c.get(url)
        project = Project.objects.get(name="TEST DELETE DELIVERABLE")
        url2 = '/deliverableListing/' + str(project.id) + '/'

        # Check if the deliverable is still existing
        deliverable_list = Deliverable.objects.filter(name="TEST DELETE DELIVERABLE")

        # Check the return message
        self.assertRedirects(response, url2, status_code=302)
        self.assertEqual(len(deliverable_list), 0)


# check_and_release_project_view Page
class CheckAndReleaseProjectViewTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate users
        test_user = ProjectPlannerUser.objects.create_user(email="test_man@itest.com",
                                                           first_name="Claude",
                                                           name="Francois",
                                                           team="Designer",
                                                           password="Chanson",
                                                           )
        test_user.save()
        test_user2 = ProjectPlannerUser.objects.create_user(email="test_man2@itest.com",
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
        deliverable = Deliverable.objects.create(name="TEST CHECK N RELEASE DELIVERABLE",
                                                 description="TEST DELIVERABLE LISTING DELIVERABLE DESCRIPTION",
                                                 project=project, )
        deliverable.contributor.add(test_user)
        deliverable.status = "APPROVED"
        deliverable.save()
        # Generate document
        document = Document.objects.create(name="TEST DELIVERABLE LISTING DOCUMENT", link="TEST LINK",
                                           deliverable=deliverable)
        document.save()

    def test_check_and_release_project_view_page(self):
        """Check the check and release a project.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Generate an url call
        project = Project.objects.get(name="TEST CHECK N RELEASE PROJECT")
        url = '/checkAndReleaseProject/' + str(project.id) + '/'
        response = c.get(url)
        url2 = '/displayProject/' + str(project.id) + '/'

        # Load again
        project = Project.objects.get(name="TEST CHECK N RELEASE PROJECT")

        # Check the return message
        self.assertRedirects(response, url2, status_code=302)
        self.assertEqual(project.status, "FINISHED")


# contributor_is_not_already_in_the_list Function
class ContributorIsNotAlreadyInTheListFunctionTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate users
        test_user = ProjectPlannerUser.objects.create_user(email="test_man@itest.com",
                                                           first_name="Claude",
                                                           name="Francois",
                                                           team="Designer",
                                                           password="Chanson",
                                                           )
        test_user.save()
        test_user2 = ProjectPlannerUser.objects.create_user(email="test_man2@itest.com",
                                                            first_name="Michel",
                                                            name="Berger",
                                                            team="Marketing",
                                                            password="Poussette",
                                                            )
        test_user2.save()
        test_user3 = ProjectPlannerUser.objects.create_user(email="test_man3@itest.com",
                                                            first_name="Georges",
                                                            name="King",
                                                            team="DOI",
                                                            password="Mouais13",
                                                            )
        test_user3.save()
        # Generate project
        project = Project.objects.create(name="TEST CHECK N RELEASE PROJECT")
        project.contributor.add(test_user)
        project.contributor.add(test_user2)
        project.save()
        # Generate deliverable
        deliverable = Deliverable.objects.create(name="TEST CHECK N RELEASE DELIVERABLE",
                                                 description="TEST DELIVERABLE LISTING DELIVERABLE DESCRIPTION",
                                                 project=project, )
        deliverable.contributor.add(test_user)
        deliverable.status = "APPROVED"
        deliverable.save()
        # Generate document
        document = Document.objects.create(name="TEST DELIVERABLE LISTING DOCUMENT", link="TEST LINK",
                                           deliverable=deliverable)
        document.save()

    def test_contributor_is_not_already_in_the_list(self):
        """Check if the user is in a list.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Generate a dynamic url
        project_created = Project.objects.get(name="TEST CHECK N RELEASE PROJECT")
        user_in_the_list = ProjectPlannerUser.objects.get(name="Berger")
        user_not_in_the_list = ProjectPlannerUser.objects.get(name="King")
        contributors = ContributorProject.objects.filter(project=project_created)
        contributor_list = []
        for contributor in contributors:
            contributor_list.append(contributor.projectPlannerUser.email)

        # Function call
        already_in_the_list = contributor_is_not_already_in_the_list(user_in_the_list, contributor_list)
        not_in_the_list = contributor_is_not_already_in_the_list(user_not_in_the_list, contributor_list)

        # Check the return message
        self.assertTrue(already_in_the_list)
        self.assertFalse(not_in_the_list)


# define_project_advancement Function
class DefineProjectAdvancementFunctionTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate users
        test_user = ProjectPlannerUser.objects.create_user(email="test_man@itest.com",
                                                           first_name="Claude",
                                                           name="Francois",
                                                           team="Designer",
                                                           password="Chanson",
                                                           )
        test_user.save()
        test_user2 = ProjectPlannerUser.objects.create_user(email="test_man2@itest.com",
                                                            first_name="Michel",
                                                            name="Berger",
                                                            team="Marketing",
                                                            password="Poussette",
                                                            )
        test_user2.save()
        # Generate project
        project = Project.objects.create(name="TEST ADVANCEMENT1")
        project.contributor.add(test_user)
        project.contributor.add(test_user2)
        project.save()
        project2 = Project.objects.create(name="TEST ADVANCEMENT2")
        project2.contributor.add(test_user)
        project2.contributor.add(test_user2)
        project2.save()
        # Generate deliverable
        deliverable = Deliverable.objects.create(name="TEST CHECK N RELEASE DELIVERABLE",
                                                 description="TEST DELIVERABLE LISTING DELIVERABLE DESCRIPTION",
                                                 project=project, )
        deliverable.contributor.add(test_user)
        deliverable.status = "APPROVED"
        deliverable.save()
        deliverable2 = Deliverable.objects.create(name="TEST CHECK N RELEASE DELIVERABLE2",
                                                  description="TEST DELIVERABLE LISTING DELIVERABLE DESCRIPTION",
                                                  project=project2, )
        deliverable2.contributor.add(test_user)
        deliverable2.save()
        # Generate document
        document = Document.objects.create(name="TEST DELIVERABLE LISTING DOCUMENT", link="TEST LINK",
                                           deliverable=deliverable)
        document.save()

    def test_define_project_advancement(self):
        """Check the advancement of a project.
        """
        # Generate a fake user
        c = Client()
        c.login(email="test_man@itest.com", password="Chanson")
        # Generate a dynamic url
        project = Project.objects.get(name="TEST ADVANCEMENT1")
        project2 = Project.objects.get(name="TEST ADVANCEMENT2")

        # Function call
        project_adv_100 = define_project_advancement(project.id)
        project_adv_0 = define_project_advancement(project2.id)

        # Check the return message
        self.assertEqual(project_adv_100, 100)
        self.assertEqual(project_adv_0, 0)


# Project model
class ProjectTest(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate user
        test_user = ProjectPlannerUser.objects.create_user(email="test_man@itest.com",
                                                           first_name="Claude",
                                                           name="Francois",
                                                           team="Designer",
                                                           password="Chanson",
                                                           )
        test_user.save()
        # Generate project
        project = Project.objects.create(name="TEST PROJECT MODEL PROJECT")
        project.contributor.add(test_user)
        project.save()
        # Generate deliverable
        deliverable = Deliverable.objects.create(name="TEST PROJECT MODEL DELIVERABLE",
                                                 description="TEST PROJECT MODEL DELIVERABLE DESCRIPTION",
                                                 project=project, )
        deliverable.contributor.add(test_user)
        deliverable.save()
        # Generate document
        document = Document.objects.create(name="TEST PROJECT MODEL DOCUMENT", link="TEST LINK",
                                           deliverable=deliverable)
        document.save()

    def create_project(self,
                       name="Project #1",
                       creation_date='2020-7-20',
                       deletion_date='2020-7-20',
                       closure_date='2020-7-20',
                       status='ONGOING',
                       advancement=1,
                       description="Description Project #1",
                       ):
        # Gather information in database
        user = ProjectPlannerUser.objects.get(name="Francois")

        # Create a deliverable
        project_test = Project.objects.create(name=name,
                                              creationDate=creation_date,
                                              deletionDate=deletion_date,
                                              closureDate=closure_date,
                                              status=status,
                                              advancement=advancement,
                                              description=description
                                              )
        project_test.contributor.add(user)

        return project_test

    def test_project_creation(self):
        project = self.create_project()
        self.assertTrue(isinstance(project, Project))


# ContributorProject model
class ContributorProjectTest(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Generate user
        test_user = ProjectPlannerUser.objects.create_user(email="test_man@itest.com",
                                                           first_name="Claude",
                                                           name="Francois",
                                                           team="Designer",
                                                           password="Chanson",
                                                           )
        test_user.save()
        # Generate project
        project = Project.objects.create(name="TEST CONTRIBUTORPROJECT MODEL PROJECT")
        project.contributor.add(test_user)
        project.save()
        # Generate deliverable
        deliverable = Deliverable.objects.create(name="TEST CONTRIBUTORPROJECT MODEL DELIVERABLE",
                                                 description="TEST CONTRIBUTORPROJECT MODEL DELIVERABLE DESCRIPTION",
                                                 project=project, )
        deliverable.contributor.add(test_user)
        deliverable.save()
        # Generate document
        document = Document.objects.create(name="TEST CONTRIBUTORPROJECT MODEL DOCUMENT", link="TEST LINK",
                                           deliverable=deliverable)
        document.save()

    def create_contributor_project(self,
                                   adding_date='2020-7-20',
                                   removing_date='2020-7-20',
                                   permission='CONTRIB'):
        # Gather information in database
        user = ProjectPlannerUser.objects.get(name="Francois")
        project = Project.objects.get(name="TEST CONTRIBUTORPROJECT MODEL PROJECT")

        # Create a deliverable
        project_test = ContributorProject.objects.create(addingDate=adding_date,
                                                         removingDate=removing_date,
                                                         permission=permission,
                                                         project=project,
                                                         projectPlannerUser=user
                                                         )
        return project_test

    def test_project_creation(self):
        contributor_project = self.create_contributor_project()
        self.assertTrue(isinstance(contributor_project, ContributorProject))