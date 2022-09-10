from django.test import SimpleTestCase
from social.forms import NewStatusPostForm

class TestForms(SimpleTestCase):

    def test_post_form_valid_data(self):
        form = NewStatusPostForm(data={
            'content': 'test post form',
            'created_by': 1
        })

        self.assertTrue(form.is_valid())

    def test_post_form_no_data(self):
        form = NewStatusPostForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)