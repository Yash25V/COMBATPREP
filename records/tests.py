from django.test import TestCase
from accounts.models import User
from .models import SoldierProfile, Assessment

class RecordsModelTests(TestCase):
    def setUp(self):
        self.officer = User.objects.create_user(username='officer1', role='OFFICER')
        self.soldier = User.objects.create_user(username='soldier1', role='SOLDIER')
        self.profile = SoldierProfile.objects.create(user=self.soldier, service_number='SN123', rank='Private')

    def test_soldier_profile_creation(self):
        self.assertEqual(self.profile.service_number, 'SN123')
        self.assertEqual(self.profile.user.username, 'soldier1')

    def test_assessment_readiness_score(self):
        assessment = Assessment.objects.create(
            soldier=self.soldier,
            officer=self.officer,
            physical_fitness_score=90,
            technical_skills_score=85,
            training_score=80
        )
        expected_score = round((90 + 85 + 80) / 3.0, 2)
        self.assertEqual(assessment.readiness_score, expected_score)

