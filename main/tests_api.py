import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Project, Experience

class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        
        self.project = Project.objects.create(
            title="Portfolio", description="My website", link="https://example.com"
        )
        
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        
        self.payload = {
            "title": "New project", "description": "A useful app", 
            "link": "https://example.com/", "image": "",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"link": "javascript:alert(1)"}, "link"), # Disesuaikan ke field 'link'
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ExperienceRolesAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com"
        )
        self.editor = User.objects.create_user(
            username="editor", password="test-password"
        )
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.editor.groups.add(editor_group)

        self.regular_user = User.objects.create_user(
            username="regular", password="test-password"
        )

        self.experience = Experience.objects.create(
            title="Magang Awal",
            description="Deskripsi magang",
            category="internship",
            started_at="2025-01-01",
            ended_at="2025-12-31"
        )

        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])

        self.payload = {
            "title": "Pengalaman Baru",
            "description": "Deskripsi baru",
            "category": "full-time",
            "started_at": "2026-01-01",
            "ended_at": "2026-12-31"
        }

    def test_public_list_detail_search_and_404(self):
        resp_list = self.client.get(self.list_url)
        self.assertEqual(resp_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp_list.data), 1)

        resp_detail = self.client.get(self.detail_url)
        self.assertEqual(resp_detail.status_code, status.HTTP_200_OK)

        resp_search = self.client.get(self.list_url, {"title": "Magang"})
        self.assertEqual(len(resp_search.data), 1)
        resp_search_empty = self.client.get(self.list_url, {"title": "Not Found"})
        self.assertEqual(len(resp_search_empty.data), 0)

        url_404 = reverse("api:experience-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url_404).status_code, status.HTTP_404_NOT_FOUND)
        
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_visitor_and_regular_user_cannot_write(self):
        for user in (None, self.regular_user):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Ubah"}, format="json").status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)

            self.assertEqual(Experience.objects.count(), 1)
            self.experience.refresh_from_db()
            self.assertEqual(self.experience.title, "Magang Awal")

    def test_editor_can_patch_put_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertEqual(self.client.delete(self.detail_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Experience.objects.filter(id=self.experience.id).exists())
        
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, status.HTTP_200_OK)
        patch_resp = self.client.patch(self.detail_url, {"title": "Diedit oleh Editor"}, format="json")
        self.assertEqual(patch_resp.status_code, status.HTTP_200_OK)
        
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Diedit oleh Editor")

    def test_owner_can_create_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        
        response_post = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        
        response_put = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response_put.status_code, status.HTTP_200_OK)

        response_patch = self.client.patch(self.detail_url, {"title": "Diedit oleh Owner"}, format="json")
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)

        response_delete = self.client.delete(self.detail_url)
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_experience_serializer_validations(self):
        self.client.force_authenticate(user=self.owner)

        resp_empty_title = self.client.post(self.list_url, {**self.payload, "title": ""}, format="json")
        self.assertEqual(resp_empty_title.status_code, status.HTTP_400_BAD_REQUEST)

        resp_xss_safe = self.client.post(self.list_url, {
            **self.payload, 
            "title": "<h1>Aman</h1>",
            "description": "<b>Teks Bold</b>", 
            "category": "internship"
        }, format="json")
        
        if resp_xss_safe.status_code != 201:
            print("\nERROR DATA:", resp_xss_safe.data)
            
        self.assertEqual(resp_xss_safe.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp_xss_safe.data["title"], "Aman")
        self.assertEqual(resp_xss_safe.data["description"], "Teks Bold")
        self.assertEqual(resp_xss_safe.data["category"], "internship")

        resp_bad_dates = self.client.post(self.list_url, {
            **self.payload, 
            "started_at": "2026-12-31", 
            "ended_at": "2026-01-01"
        }, format="json")
        self.assertEqual(resp_bad_dates.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ended_at", resp_bad_dates.data)

    def test_session_write_csrf_experience(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        
        response_no_csrf = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response_no_csrf.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Experience.objects.count(), 1)

        client.get(self.list_url, HTTP_ACCEPT="text/html")
        token = client.cookies["csrftoken"].value
        response_with_csrf = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response_with_csrf.status_code, status.HTTP_201_CREATED)

    def test_experience_star_toggles(self):
        star_url = reverse("api:experience-star", args=[self.experience.id])
        self.assertEqual(self.client.post(star_url).status_code, status.HTTP_403_FORBIDDEN)
        
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)