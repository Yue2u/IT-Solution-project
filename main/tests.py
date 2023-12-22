from django.test import Client, TestCase
from django.http import HttpResponse, HttpResponseNotAllowed
from .models import Text


class TestRuntext(TestCase):
    def setUp(self):
        self.client = Client()
        self.texts = [
            "Test text 1",
            "Test text 2",
            "Short",
            "Some long text here hmmmm very long text idk who is going to read it at all",
            "Русский текст",
            "Text with /?*=,.<>",
            "Русский текст с /*?=,.<>",
            ]

    def test_allowed_methods(self):
        data = {"text": self.texts[0]}
        post_response = self.client.post('/runtext/', data=data)
        put_response = self.client.put('/runtext/', data=data)
        patch_response = self.client.patch('/runtext/', data=data)
        delete_response = self.client.delete('/runtext/', data=data)
        get_response = self.client.get('/runtext/', data=data)

        self.assertIsInstance(post_response, HttpResponseNotAllowed)
        self.assertIsInstance(put_response, HttpResponseNotAllowed)
        self.assertIsInstance(patch_response, HttpResponseNotAllowed)
        self.assertIsInstance(delete_response, HttpResponseNotAllowed)

        self.assertIsInstance(get_response, HttpResponse)
        self.assertNotIsInstance(get_response, HttpResponseNotAllowed)

    def test_empty_data(self):
        texts_count_old = Text.objects.count()
        response = self.client.get('/runtext/')
        texts_count_new = Text.objects.count()

        self.assertIsInstance(response, HttpResponse)
        self.assertNotIsInstance(response, HttpResponseNotAllowed)
        self.assertEqual(texts_count_old, texts_count_new)
        self.assertEqual(response.headers.get("Content-Disposition"),
                         "attachment; filename=runtext_video.avi")

    def test_not_empty(self):
        data = {"text": self.texts[0]}
        texts_count_old = Text.objects.count()
        response = self.client.get('/runtext/', data=data)
        texts_count_new = Text.objects.count()
        created_text = Text.objects.get(pk=1)

        self.assertIsInstance(response, HttpResponse)
        self.assertNotIsInstance(response, HttpResponseNotAllowed)
        self.assertEqual(texts_count_old + 1, texts_count_new)
        self.assertEqual(created_text.text, self.texts[0])
        self.assertEqual(response.headers.get("Content-Disposition"),
                         "attachment; filename=runtext_video.avi")

    def test_short_text(self):
        data = {"text": self.texts[2]}
        texts_count_old = Text.objects.count()
        response = self.client.get('/runtext/', data=data)
        texts_count_new = Text.objects.count()
        created_text = Text.objects.get(pk=1)

        self.assertIsInstance(response, HttpResponse)
        self.assertNotIsInstance(response, HttpResponseNotAllowed)
        self.assertEqual(texts_count_old + 1, texts_count_new)
        self.assertEqual(created_text.text, self.texts[2])
        self.assertEqual(response.headers.get("Content-Disposition"),
                         "attachment; filename=runtext_video.avi")

    def test_long_text(self):
        data = {"text": self.texts[3]}
        texts_count_old = Text.objects.count()
        response = self.client.get('/runtext/', data=data)
        texts_count_new = Text.objects.count()
        created_text = Text.objects.get(pk=1)

        self.assertIsInstance(response, HttpResponse)
        self.assertNotIsInstance(response, HttpResponseNotAllowed)
        self.assertEqual(texts_count_old + 1, texts_count_new)
        self.assertEqual(created_text.text, self.texts[3])
        self.assertEqual(response.headers.get("Content-Disposition"),
                         "attachment; filename=runtext_video.avi")

    def test_russian_text(self):
        data = {"text": self.texts[4]}
        texts_count_old = Text.objects.count()
        response = self.client.get('/runtext/', data=data)
        texts_count_new = Text.objects.count()
        created_text = Text.objects.get(pk=1)

        self.assertIsInstance(response, HttpResponse)
        self.assertNotIsInstance(response, HttpResponseNotAllowed)
        self.assertEqual(texts_count_old + 1, texts_count_new)
        self.assertEqual(created_text.text, self.texts[4])
        self.assertEqual(response.headers.get("Content-Disposition"),
                         "attachment; filename=runtext_video.avi")

    def test_punct_text(self):
        texts_count_old = Text.objects.count()
        response1 = self.client.get('/runtext/',
                                   data={"text": self.texts[5]})
        texts_count_new1 = Text.objects.count()
        response2 = self.client.get('/runtext/',
                                   data={"text": self.texts[6]})
        texts_count_new2 = Text.objects.count()
        created_text1 = Text.objects.get(pk=1)
        created_text2 = Text.objects.get(pk=2)

        self.assertIsInstance(response1, HttpResponse)
        self.assertNotIsInstance(response1, HttpResponseNotAllowed)
        self.assertIsInstance(response2, HttpResponse)
        self.assertNotIsInstance(response2, HttpResponseNotAllowed)
        self.assertEqual(texts_count_old + 1, texts_count_new1)
        self.assertEqual(texts_count_old + 2, texts_count_new2)
        self.assertEqual(created_text1.text, self.texts[5])
        self.assertEqual(created_text2.text, self.texts[6])
        self.assertEqual(response1.headers.get("Content-Disposition"),
                         "attachment; filename=runtext_video.avi")
        self.assertEqual(response2.headers.get("Content-Disposition"),
                         "attachment; filename=runtext_video.avi")
