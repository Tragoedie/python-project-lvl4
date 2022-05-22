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
            password='test_pass_1',
        )
        user_simple.save()
        user_protected = CustomUser.objects.create(
            first_name='name_2',
            last_name='last_name_2',
            username='test_user_2',
            password='test_pass_2',
        )
        user_protected.save()
        status_test = Status.objects.create(
            name='status_test',
        )
        Task.objects.create(
            name='task_test',
            status=status_test,
            tasks_author=user_protected,
            tasks_executor=user_protected,
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
            'password1': 'test_pass_3',
            'password2': 'test_pass_3',
        }
        response = self.client.post(
            reverse('user_register'),
            user_new,
            follow=True,
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'User successfully registered',
        )
        self.assertRedirects(response, 'user_login', status_code=CODE_REDIRECT)

        user_new = CustomUser.objects.get(pk=3)
        self.assertEqual(user_new.first_name, 'name_3')
        self.assertEqual(user_new.last_name, 'last_name_3')
        self.assertEqual(user_new.username, 'test_user_3')
        self.assertTrue(user_new.check_password('test_pass_3'))
