from django.test import TestCase
from django.urls import reverse

CODE_OK = 200


class MainPageTestCase(TestCase):

    def test_main_page(self):
        response = self.client.get(reverse('main_page'))
        self.assertEqual(response.status_code, CODE_OK)
        self.assertTemplateUsed(response, template_name='main_page.html')
