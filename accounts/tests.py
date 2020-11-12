from unittest.mock import MagicMock

from django.core.mail.message import EmailMessage
from django.test import TestCase, Client
from django.urls import reverse
from django_forms_test import FormTest, field

from accounts.forms import MyUserAdminCreationForm, RegisterForm
from accounts.function_for_accounts import send_notifications_to_contributor
from accounts.models import ProjectPlannerUser


# my_account_view page
from project.models import Deliverable, Project


class AccountPageTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Creation of an user
        test_user = ProjectPlannerUser. \
            objects.create_user(email="test_man@itest.com",
                                first_name="Claude",
                                name="Francois",
                                team="Designer",
                                password="Chanson",
                                )
        test_user.save()

    # test page returns 200
    def test_account_page_return_200_when_user_is_connected(self):
        """
        Check if once connected, the user has access to his profile page.
        :return:
        """

        # Authenticate an user
        self.client.login(username="test_man@itest.com",
                          password="Chanson")
        # Look for the page
        response = self.client.get(reverse('accounts:myAccount'))

        # Check page
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'test_man@itest.com')
        self.assertTemplateUsed('accounts/myAccount.html')

    # test page doesn't return 200
    def test_account_page_return_200_when_user_is_not_connected(self):
        """
        Check if not connected, the user has access to his profile page.
        :return:
        """
        response = self.client.get(reverse('accounts:myAccount'))

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)


# my_contribution_view page
class MyContributionPageTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Creation of an user
        test_user = ProjectPlannerUser.objects. \
            create_user(email="test_man@itest.com",
                        first_name="Claude",
                        name="Francois",
                        team="Designer",
                        password="Chanson",
                        )
        test_user.save()

    # test page returns 200
    def test_contribution_page_return_200_when_user_is_connected(self):
        """
        Check if once connected, the user has access to his profile page.
        :return:
        """

        # Authenticate an user
        self.client.login(username="test_man@itest.com",
                          password="Chanson")
        # Look for the page
        response = self.client.get(reverse('accounts:myContribution'))

        # Check page
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'test_man@itest.com')
        self.assertTemplateUsed('accounts/myContribution.html')

    # test page doesn't return 200
    def test_contribution_page_return_200_when_user_is_not_connected(self):
        """
        Check if not connected, the user has access to his profile page.
        :return:
        """
        response = self.client.get(reverse('accounts:myContribution'))

        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)


# signup_view page
class SignupPageTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Creation of an user
        test_user = ProjectPlannerUser.objects. \
            create_user(email="hubert.f@gmail.com",
                        first_name="hubert",
                        name="font",
                        team="Designer",
                        password="Chanson",
                        )
        test_user.save()

    # test page returns a 200
    def test_signup_page_return_200_on_GET_method(self):
        """
        Check the access to the page.
        :return:
        """
        response = self.client.get(reverse('accounts:signUp'))

        # Check
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/signUp.html',)

    # test page returns a 200
    def test_signup_page_return_200_on_POST_method(self):
        """
        Check the success of the access of the sign up.
        :return:
        """
        # Request comes with authentication data
        response = self.client.post(reverse('accounts:signUp'),
                                    data={'email': 'jojo@gigi.com',
                                          'first_name': 'Joan',
                                          'name': 'JO',
                                          'team': 'Designer',
                                          'Password': 'Lolilol',
                                          'Password confirmation': 'Lolilol'}
                                    )

        self.assertEqual(response.status_code, 200)


# login_view page
class LoginPageTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Creation of an user
        test_user = ProjectPlannerUser.objects. \
            create_user(email='hubert.f@gmail.com',
                        first_name="Claude",
                        name="Francois",
                        team="Designer",
                        password='hubert',
                        )
        test_user.save()

    # test page returns a 200
    def test_login_page_return_200_on_GET_method(self):
        """
        Check the success of the access of the log in.
        :return:
        """
        response = self.client.get(reverse('accounts:logIn'))

        # Check
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/logIn.html')

    # test page returns a 302
    def test_login_page_return_302_with_a_POST_method(self):
        """
        Check the right connection function.
        :return:
        """
        # Request comes with authentication data
        c = Client()
        response = c.post('/accounts/logIn/',
                          data={'username': 'hubert.f@gmail.com',
                                'password': 'hubert'}
                          )
        self.assertTemplateUsed('accounts/myContribution.html')


# logout_view page
class LogoutPageTestCase(TestCase):

    def setUp(self):
        """ Set up variables before launching tests.
        """
        # Creation of an user
        test_user = ProjectPlannerUser.objects. \
            create_user(email="test_man@itest.com",
                        first_name="Claude",
                        name="Francois",
                        team="Designer",
                        password="Chanson",
                        )
        test_user.save()

        # Authenticate an user
        self.client.login(username="test_man@itest.com", password="Chanson")

    # test that page returns a 200
    def test_logout_page_return_200_when_user_is_connected(self):
        """
        Check the log out.
        :return:
        """
        # Disconnect the user
        response = self.client.get(reverse('accounts:logOut'))
        # Check that an user is connected
        self.assertNotEqual(str(response.context['user']),
                            "test_man@itest.com")

        self.assertEqual(response.status_code, 200)

    # test that page returns a 200
    def test_logout_page_return_200_when_user_not_connected(self):
        """
        Check the log out.
        :return:
        """
        response = self.client.get(reverse('accounts:logOut'))

        self.assertEqual(response.status_code, 200)

    # test django flash message
    def test_django_flash_messages(self):
        """
        Check the log out message.
        :return:
        """

        response = self.client.get(reverse('accounts:logOut'))
        messages = list(response.context['messages'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(messages[0]), 'Bye bye!')


# MyUser models
class MyUserTest(TestCase):

    # Models
    def test_create_myUser(self, email="test_man@itest.com",
                           first_name="Claude",
                           name="Francois",
                           team="Designer",
                           ):

        return ProjectPlannerUser.objects.create_user(email=email,
                                                      first_name=first_name,
                                                      name=name,
                                                      team=team,
                                                      password=None,
                                                      )

    def test_myUser_creation(self):
        user = self.test_create_myUser()
        self.assertTrue(isinstance(user, ProjectPlannerUser))


# RegisterForm form
class RegisterFormTest(FormTest):

    form = RegisterForm
    required_fields = [
        ('email', field.EMAIL),
        ('password', field.PASSWORD),
        ('password2', field.PASSWORD),
    ]


# MyUserAdminCreationForm form
class MyUserAdminCreationFormTest(FormTest):
    form = MyUserAdminCreationForm
    required_fields = [
        ('email', field.EMAIL),
        ('password1', field.PASSWORD),
        ('password2', field.PASSWORD),
    ]


# Function for accounts
class FunctionForAccounts(TestCase):

    def test_send_notifications_to_contributor_project(self):
        # Creation of an user
        test_user = ProjectPlannerUser.objects. \
            create(email="test_man@itest.com",
                   first_name="Claude",
                   name="Francois",
                   team="Designer",
                   password="Chanson",
                   )
        test_user.save()

        # Creation of an project
        test_project = Project.objects.create(name="Test Project #1")
        test_project.save()
        test_project.contributor.add(test_user)

        print(test_user)

        # Mock EmailMessage.send function
        EmailMessage.send = MagicMock(return_value=0)

        # Test the function
        message = send_notifications_to_contributor(test_project)
        print(message)

        self.assertTrue(message, "Successfully !")

    def test_send_notifications_to_contributor_deliverable(self):
        # Creation of an user
        test_user = ProjectPlannerUser.objects. \
            create(email="test_man3@itest.com",
                   first_name="Claude",
                   name="Francois",
                   team="Designer",
                   password="Chanson",
                   )
        test_user.save()

        # Creation of an project
        test_project = Project.objects.create(name="Test Project #2")
        test_project.save()
        test_project.contributor.add(test_user)

        # Creation of an deliverable
        test_deliverable = Deliverable.objects. \
            create(name="Test Deliverable #2",
                   project=test_project)
        test_deliverable.save()
        test_deliverable.contributor.add(test_user)

        # Test the function
        send_notifications_to_contributor(test_deliverable)

