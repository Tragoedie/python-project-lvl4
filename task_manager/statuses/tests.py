from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import CustomUser

CODE_OK = 200
CODE_REDIRECT = 302


class StatusTestCase(TestCase):

    def setUp(self):
        user_test = CustomUser.objects.create(
            first_name='name_1',
            last_name='last_name_1',
            username='test_user_1',
            password='bj0epvTN',
        )
        user_test.save()
        status_test = Status.objects.create(
            name='status_test',
        )
        Task.objects.create(
            name='task_test',
            status=status_test,
            tasks_author=user_test,
            executor=user_test,
        )
        self.client.force_login(user_test)

    def test_statuses_list(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, CODE_OK)
        self.assertTemplateUsed(response, template_name='statuses_list.html')
        statuses_list = list(response.context['statuses_list'])
        status_test = statuses_list[0]
        self.assertEqual(status_test.name, 'status_test')
        self.assertEqual(status_test.id, 1)

    def test_status_create(self):
        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, CODE_OK)
        self.assertTemplateUsed(response, template_name='status_create.html')
        status_create = {'name': 'status_test_2'}
        response = self.client.post(
            reverse('status_create'),
            data=status_create,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Status successfully created.',
        )
        self.assertEqual(response.status_code, CODE_REDIRECT)
        self.assertEqual(Status.objects.get(pk=2).name, 'status_test_2')

    def test_status_update(self):
        response = self.client.get(reverse('status_update', args='1'))
        self.assertEqual(response.status_code, CODE_OK)
        self.assertTemplateUsed(response, template_name='status_update.html')
        status_update = {'name': 'status_update'}
        response = self.client.post(
            reverse('status_update', args='1'),
            data=status_update,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Status successfully changed.',
        )
        self.assertEqual(response.status_code, CODE_REDIRECT)
        self.assertEqual(Status.objects.get(pk=1).name, 'status_update')

    def test_status_delete(self):
        Status.objects.create(name='status_test_2')
        response = self.client.get(reverse('status_delete', args='2'))
        self.assertEqual(response.status_code, CODE_OK)
        self.assertTemplateUsed(response, template_name='status_delete.html')
        response = self.client.post(reverse('status_delete', args='2'))
        self.assertEqual(response.status_code, CODE_REDIRECT)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Status successfully deleted.',
        )
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(pk=2)

    def test_status_busy_delete(self):
        response = self.client.post(reverse('status_delete', args='1'))
        self.assertEqual(response.status_code, CODE_REDIRECT)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Can not delete this status - because it is in use.',
        )
