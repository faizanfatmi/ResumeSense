from django.test import TestCase
from apps.jobmatcher.services.job_matcher import match_resume_to_job


class JobMatcherTests(TestCase):
    def test_job_description_matching(self):
        resume = "Software engineer proficient in Python, SQL, Docker, and Django. Experienced in backend development."
        jd = "Seeking a Python Engineer with strong knowledge of Python, Django, SQL, and AWS."

        res = match_resume_to_job(resume, jd)
        self.assertIn('Python', res.matched_skills)
        self.assertIn('Django', res.matched_skills)
        self.assertIn('Sql', [s.title() for s in res.matched_skills])
        self.assertIn('Aws', [s.title() for s in res.missing_skills])
        self.assertGreater(res.match_score, 40)
        self.assertTrue(len(res.suggestions) > 0)
