from django.test import TestCase
from .models import Post
from django.urls import reverse
from django.contrib.auth import get_user_model

class PostCRUDTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'test@testmail.com',
            passsword = 'secret',
        )
        self.post = Post.objects.create(
            title='test post',
            body='test body',
            author=self.user,
        )

    def test_body_content(self):
        post = Post.objects.get(id=1)
        expected_object_name = f"{post.body}"
        self.assertEqual(expected_object_name, "Test")

    def test_listview_url_by_name(self):
        resp = self.client.get(reverse("posts_list"))
        self.assertEqual(resp.status_code, 200)

    def test_post_list_view(self):
        response = self.client.get("/posts/")
        self.assertEqual(response.status_code, 200)
        response2 = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A title")
        self.assertContains(response, "A body")
        self.assertTemplateUsed(response, "posts/list.html")
        self.assertTemplateUsed(response, "base.html")

    def test_post_detail_view(self):
        response = self.client.get("/posts/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A title")
        self.assertTemplateUsed(response, "posts/detail.html")

    def test_post_create_view(self):
        response = self.client.post(reverse("post_new"), {
            "title": "New title",
            "body": "New body",
            "author": self.user.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "New title")
        self.assertEqual(Post.objects.last().body, "New body")
        self.assertTemplateUsed(response, "posts/new.html")

    def test_post_update_view(self):
        response = self.client.post(reverse("post_edit", args=[1]), {
            "title": "Updated title",
            "body": "Updated body"

        })
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):
        response = self.client.post(reverse("post_delete", args=[1]))
        self.assertEqual(response.status_code, 302)



# class PostViewTest(TestCase):
#     def setUp(self):
#         Post.objects.create(title="Another Test", body="Test2")
        
#     def test_listview_url_exists_at_proper_location(self):
#         resp = self.client.get("/posts/")
#         self.assertEqual(resp.status_code, 200)

#     def test_detailview_exists_at_proper_location(self):
#         resp = self.client.get("/posts/1/")
#         self.assertEqual(resp.status_code, 200)

    


