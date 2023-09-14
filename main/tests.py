from django.test import TestCase, Client

from django.contrib.auth.models import User
from .models import user_data, categories, job_offers, languages, contactRequests, applications
# Create your tests here.

class Tests(TestCase):

    def setUp(self):

        testCategory = categories.objects.create(name="testCategory")
        testCategory2 = categories.objects.create(name="testCategory2")

        testLanguage = languages.objects.create(name="testLanguage")
        testLanguage2 = languages.objects.create(name="testLanguage2")

        testUser = User.objects.create_user(
                    username="testUsername", 
                    email="test@example.com", 
                    password="123Password", 
                    first_name="testFirstName", 
                    last_name="testLastName")
        
        testUser2 = User.objects.create_user(
                username="testUsername2", 
                email="test2@example.com", 
                password="123Password", 
                first_name="testFirstName2", 
                last_name="testLastName2")


        testJobListing = job_offers.objects.create(
            user = testUser,
            title = "Test job title",
            category = testCategory,
            pay = "1234€",
            languages = testLanguage,
            company = "testCompany",
            description = "testDescription",
        )

        testApplication = applications.objects.create(
            user_id = testUser2, 
            job_offer_id = testJobListing
            )
        
        testApplication2 = applications.objects.create(
            user_id = testUser, 
            job_offer_id = testJobListing
        )
        
        testContactRequest = contactRequests.objects.create(
            first_name = "testFirstname",
            last_name = "testLastname",
            email = "test@example.com",
            phone_number = "00001111111",
            content = "Test text for the test contactRequest"
        )


    def test_categories_count_all(self):
        c = categories.objects.all()
        self.assertEqual(c.count(), 2)

    def test_languages_count_all(self):
        c = languages.objects.all()
        self.assertEqual(c.count(), 2)

    def test_valid_application(self):
        u = User.objects.get(username="testUsername2")
        a = applications.objects.get(user_id = u)
        self.assertTrue(a.valid_user())

    def test_valid_application_false(self):
        u = User.objects.get(username="testUsername")
        a = applications.objects.get(user_id = u)
        self.assertFalse(a.valid_user())

    def test_valid_contact(self):
        c = contactRequests.objects.get(first_name = "testFirstname")
        self.assertTrue(c.valid_request())



    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)

    def test_jobs(self):
        c = Client()
        response = c.get("/jobs")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["jobs"].count(), 1)

    def test_contact(self):
        c = Client()
        response = c.get("/contact")
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        c = Client()
        response = c.get("/login")
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        c = Client()
        response = c.get("/logout")
        self.assertEqual(response.status_code, 200)
            
    def test_register(self):
        c = Client()
        response = c.get("/register")
        self.assertEqual(response.status_code, 200)

    def test_specific_job(self):
        testUser = User.objects.get(username="testUsername")
        testJob = job_offers.objects.get(user_id = testUser)

        c = Client()
        response = c.get(f"/jobs/{testJob.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_specific_id(self):
        max_id = job_offers.objects.all().count()
        c = Client()
        response = c.get(f"/jobs/{max_id + 1}")
        self.assertEqual(response.context["message"], "Error, couldn't find job. Please try agian.")