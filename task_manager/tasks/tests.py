from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import CustomUser

CODE_OK = 200
CODE_REDIRECT = 302


class TaskTestCase(TestCase):

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
            executor=user_test,
        )
        task_test.labels.add(label_test)
        self.client.force_login(user_test)

    def test_tasks_list(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, CODE_OK)
        self.assertTemplateUsed(response, template_name='tasks_list.html')
        task_list = list(response.context['tasks_list'])
        task_test = task_list[0]
        self.assertEqual(task_test.name, 'task_test')
        self.assertEqual(task_test.id, 1)
        self.assertEqual(task_test.status.name, 'status_test')
        self.assertEqual(task_test.tasks_author.username, 'test_user_1')

    def test_task_create(self):
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, CODE_OK)
        self.assertTemplateUsed(response, template_name='task_create.html')
        task_create = {
            'name': 'task_test_2',
            'status': 1,
            'labels': 1,
        }
        response = self.client.post(
            reverse('task_create'),
            data=task_create,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Task successfully created.',
        )
        task_created = Task.objects.get(pk=2)
        self.assertEqual(response.status_code, CODE_REDIRECT)
        self.assertEqual(task_created.name, 'task_test_2')
        self.assertEqual(task_created.tasks_author.username, 'test_user_1')
        self.assertEqual(task_created.status.name, 'status_test')
        self.assertEqual(task_created.labels.all()[0].name, 'label_test')

    def test_task_update(self):
        Status.objects.create(name='status_update')
        response = self.client.get(reverse('task_update', args='1'))
        self.assertEqual(response.status_code, CODE_OK)
        self.assertTemplateUsed(response, template_name='task_update.html')
        task_update = {
            'name': 'task_update',
            'description': 'task_update',
            'status': 2,
            'executor': 1,
        }
        response = self.client.post(
            reverse('task_update', args='1'),
            data=task_update,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Task successfully changed.',
        )
        self.assertEqual(response.status_code, CODE_REDIRECT)
        self.assertEqual(Task.objects.get(pk=1).name, 'task_update')
        self.assertEqual(Task.objects.get(pk=1).description, 'task_update')
        self.assertEqual(Task.objects.get(pk=1).status.name, 'status_update')
        self.assertEqual(
            Task.objects.get(pk=1).executor.username,
            'test_user_1',
        )

    def test_task_delete(self):
        response = self.client.get(reverse('task_delete', args='1'))
        self.assertEqual(response.status_code, CODE_OK)
        self.assertTemplateUsed(response, template_name='task_delete.html')
        response = self.client.post(reverse('task_delete', args='1'))
        self.assertEqual(response.status_code, CODE_REDIRECT)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            'Task successfully deleted.',
        )
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=1)

    def test_task_delete_another_author(self):
        test_user_2 = CustomUser.objects.create(
            first_name='name_2',
            last_name='last_name_2',
            username='test_user_2',
            password='Wwk9vxl7',
        )
        test_user_2.save()
        Task.objects.create(
            name='task_test_2',
            status=Status.objects.get(pk=1),
            tasks_author=test_user_2,
        )
        url = reverse('task_delete', args='2')
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, '/tasks/')
        self.assertContains(response, 'The task can only be deleted by its author.')

    def test_task_detail(self):
        task_test = Task.objects.get(pk=1)
        response = self.client.get(reverse('task_details', args='1'))
        self.assertEqual(response.status_code, CODE_OK)
        self.assertTemplateUsed(response, template_name='task_details.html')
        self.assertContains(response, task_test.name)
        self.assertContains(response, task_test.description)
        self.assertContains(response, task_test.tasks_author)
        self.assertContains(response, task_test.status)

    def test_filter_by_status(self):
        filter_by_status = '{0}?status=1&tasks_executor=&labels='.format(reverse('tasks'))
        response = self.client.get(filter_by_status)
        self.assertEqual(response.status_code, CODE_OK)
        self.assertQuerysetEqual(list(response.context['tasks_list']), [Task.objects.get(pk=1)])

    def test_filter_by_executor(self):
        filter_by_executor = '{0}?status=&tasks_executor=1&labels='.format(reverse('tasks'))
        response = self.client.get(filter_by_executor)
        self.assertEqual(response.status_code, CODE_OK)
        self.assertQuerysetEqual(list(response.context['tasks_list']), [Task.objects.get(pk=1)])

    def test_filter_by_label(self):
        filter_by_label = '{0}?status=&tasks_executor=&labels=1'.format(reverse('tasks'))
        response = self.client.get(filter_by_label)
        self.assertEqual(response.status_code, CODE_OK)
        self.assertQuerysetEqual(list(response.context['tasks_list']), [Task.objects.get(pk=1)])

    def test_filter_by_own_tasks(self):
        filter_by_own_tasks = '{0}?status=&executor=&label=&self_tasks=on'.format(reverse('tasks'))
        response = self.client.get(filter_by_own_tasks)
        self.assertEqual(response.status_code, CODE_OK)
        self.assertQuerysetEqual(list(response.context['tasks_list']), [Task.objects.get(pk=1)])
