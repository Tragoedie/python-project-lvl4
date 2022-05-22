from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import CustomUser

CODE_OK = 200
CODE_REDIRECT = 302


class LabelTestCase(TestCase):

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
        label_test = Label.objects.create(
            name='label_test',
        )
        task_test = Task.objects.create(
            name='task_test',
            status=status_test,
            tasks_author=user_test,
        )
        task_test.labels.add(label_test)
        self.client.force_login(user_test)

    def test_labels_list(self):
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, CODE_OK)
        self.assertTemplateUsed(response, template_name='labels_list.html')
        labels_list = list(response.context['labels_list'])
        label_test = labels_list[0]
        self.assertEqual(label_test.name, 'label_test')
        self.assertEqual(label_test.id, 1)

    def test_label_create(self):
        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, CODE_OK)
        self.assertTemplateUsed(response, template_name='label_create.html')
        label_create = {'name': 'label_test_2'}
        response = self.client.post(
            reverse('label_create'),
            data=label_create,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Label successfully created.',
        )
        self.assertEqual(response.status_code, CODE_REDIRECT)
        self.assertEqual(Label.objects.get(pk=2).name, 'label_test_2')

    def test_label_update(self):
        response = self.client.get(reverse('label_update', args='1'))
        self.assertEqual(response.status_code, CODE_OK)
        self.assertTemplateUsed(response, template_name='label_update.html')
        label_update = {'name': 'label_update'}
        response = self.client.post(
            reverse('label_update', args='1'),
            data=label_update,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Label successfully changed.',
        )
        self.assertEqual(response.status_code, CODE_REDIRECT)
        self.assertEqual(Label.objects.get(pk=1).name, 'label_update')

    def test_label_delete(self):
        Label.objects.create(name='label_test_2')
        response = self.client.get(reverse('label_delete', args='2'))
        self.assertEqual(response.status_code, CODE_OK)
        self.assertTemplateUsed(response, template_name='label_delete.html')
        response = self.client.post(reverse('label_delete', args='2'))
        self.assertEqual(response.status_code, CODE_REDIRECT)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Label successfully deleted.',
        )
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(pk=2)

    def test_label_busy_delete(self):
        response = self.client.post(reverse('label_delete', args='1'))
        self.assertEqual(response.status_code, CODE_REDIRECT)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Can not delete this label - because it is in use.',
        )
