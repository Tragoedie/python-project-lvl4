from django.contrib.auth import get_user
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import CustomUser

CODE_OK = 200
CODE_REDIRECT = 302


class UserTestCase(TestCase):

    def setUp(self):
        user_simple = CustomUser.objects.create(
            first_name='name_1',
            last_name='last_name_1',
            username='test_user_1',
            password='bj0epvTN',
        )
        user_simple.save()
        user_protected = CustomUser.objects.create(
            first_name='name_2',
            last_name='last_name_2',
            username='test_user_2',
            password='Wwk9vxl7',
        )
        user_protected.save()
        status_test = Status.objects.create(
            name='status_test',
        )
        Task.objects.create(
            name='task_test',
            status=status_test,
            tasks_author=user_protected,
            executor=user_protected,
        )

    def test_users_list(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, CODE_OK)
        self.assertTemplateUsed(response, template_name='users_list.html')
        user_first = CustomUser.objects.get(pk=1)
        self.assertEqual(user_first.username, 'test_user_1')
        self.assertEqual(user_first.first_name, 'name_1')
        self.assertEqual(user_first.last_name, 'last_name_1')
        user_second = CustomUser.objects.get(pk=2)
        self.assertEqual(user_second.username, 'test_user_2')
        self.assertEqual(user_second.first_name, 'name_2')
        self.assertEqual(user_second.last_name, 'last_name_2')

    def test_user_register(self):
        response = self.client.get(reverse('user_register'))
        self.assertEqual(response.status_code, CODE_OK)
        self.assertTemplateUsed(response, template_name='user_register.html')
        user_new = {
            'first_name': 'name_3',
            'last_name': 'last_name_3',
            'username': 'test_user_3',
            'password1': 'Nx7sDQ9D',
            'password2': 'Nx7sDQ9D',
        }
        response = self.client.post(
            reverse('user_register'),
            data=user_new,
            follow=True,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'User successfully registered.',
        )
        self.assertRedirects(response, '/login/', status_code=CODE_REDIRECT)
        user_new = CustomUser.objects.get(pk=3)
        self.assertEqual(user_new.first_name, 'name_3')
        self.assertEqual(user_new.last_name, 'last_name_3')
        self.assertEqual(user_new.username, 'test_user_3')
        self.assertTrue(user_new.check_password('Nx7sDQ9D'))

    def test_user_login(self):
        response = self.client.get(reverse('user_login'))
        self.assertEqual(response.status_code, CODE_OK)
        self.assertTemplateUsed(response, template_name='user_login.html')
        user_data = {
            'username': 'test_user_1',
            'password': 'bj0epvTN',
        }
        response = self.client.post(
            reverse('user_login'),
            data=user_data,
        )
#       self.assertRedirects(resp, TASKS_LIST_URL)
#        messages = list(get_messages(response.wsgi_request))
#        self.assertEqual(
#            str(messages[0]),
#            'You are logged in.',
#        )

    def test_user_logout(self):
        self.client.force_login(CustomUser.objects.get(pk=1))
        response = self.client.post(reverse('user_logout'))
        self.assertEqual(response.status_code, CODE_REDIRECT)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'You are logged out.',
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_user_update_another_user(self):
        self.client.force_login(CustomUser.objects.get(pk=1))
        response = self.client.get(reverse('user_update', args='2'))
        self.assertEqual(response.status_code, CODE_REDIRECT)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'You have not permission to change another user.',
        )

    def test_user_update(self):
        self.client.force_login(CustomUser.objects.get(pk=1))
        response = self.client.get(reverse('user_update', args='1'))
        self.assertEqual(response.status_code, CODE_OK)
        self.assertTemplateUsed(response, template_name='user_update.html')
        user_update = {
            'first_name': 'test_update',
            'last_name': 'test_update',
            'username': 'test_update',
            'password1': 'BIWUQWIp',
            'password2': 'BIWUQWIp',
        }
        response = self.client.post(
            reverse('user_update', args='1'),
            user_update,
        )
        self.assertEqual(response.status_code, CODE_REDIRECT)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'User successfully changed',
        )
        self.assertEqual(CustomUser.objects.get(pk=1).first_name, 'test_update')
        self.assertEqual(CustomUser.objects.get(pk=1).last_name, 'test_update')
        self.assertEqual(CustomUser.objects.get(pk=1).username, 'test_update')
        self.assertTrue(CustomUser.objects.get(pk=1).check_password('BIWUQWIp'))

    def test_user_delete(self):
        self.client.force_login(CustomUser.objects.get(pk=1))
        response = self.client.get(reverse('user_delete', args='1'))
        self.assertEqual(response.status_code, CODE_OK)
        self.assertTemplateUsed(response, template_name='user_delete.html')
        response = self.client.post(reverse('user_delete', args='1'))
        self.assertEqual(response.status_code, CODE_REDIRECT)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'User successfully deleted.',
        )
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(pk=1)

    def test_user_delete_another_user(self):
        self.client.force_login(CustomUser.objects.get(pk=1))
        response = self.client.get(reverse('user_delete', args='2'))
        self.assertEqual(response.status_code, CODE_REDIRECT)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'You have not permission to change another user.',
        )

    def test_user_delete_busy_user(self):
        self.client.force_login(CustomUser.objects.get(pk=2))
        response = self.client.post(reverse('user_delete', args='2'))
        self.assertEqual(response.status_code, CODE_REDIRECT)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'You can not delete this user - because it is in use.',
        )
