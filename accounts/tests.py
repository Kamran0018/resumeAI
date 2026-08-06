from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, CandidateProfile, RecruiterProfile

class LoginAuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create test candidate user
        self.candidate = User.objects.create_user(
            username='testcandidate',
            email='candidate@example.com',
            password='Password123!',
            user_type='candidate'
        )
        CandidateProfile.objects.create(
            user=self.candidate,
            first_name='Test',
            last_name='Candidate'
        )
        
        # Create test recruiter user
        self.recruiter = User.objects.create_user(
            username='testrecruiter',
            email='recruiter@example.com',
            password='Password123!',
            user_type='recruiter'
        )
        RecruiterProfile.objects.create(
            user=self.recruiter,
            company='Tech Corp',
            position='HR Lead'
        )

    def test_candidate_login_with_username(self):
        response = self.client.post(reverse('login_candidate'), {
            'username': 'testcandidate',
            'password': 'Password123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_candidate_login_with_email(self):
        response = self.client.post(reverse('login_candidate'), {
            'username': 'candidate@example.com',
            'password': 'Password123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_recruiter_login_with_username(self):
        response = self.client.post(reverse('login_recruiter'), {
            'username': 'testrecruiter',
            'password': 'Password123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_recruiter_login_with_email(self):
        response = self.client.post(reverse('login_recruiter'), {
            'username': 'recruiter@example.com',
            'password': 'Password123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_invalid_password(self):
        response = self.client.post(reverse('login_candidate'), {
            'username': 'testcandidate',
            'password': 'WrongPassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username/email or password')
