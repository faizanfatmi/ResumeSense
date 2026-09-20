from django.test import TestCase
from apps.analysis.services.keyword_analyzer import analyze_keywords
from apps.analysis.services.score_calculator import calculate_ats_score
from apps.analysis.services.resume_analyzer import extract_contact_info, detect_sections


class AnalysisEngineTests(TestCase):
    def test_keyword_extraction(self):
        sample_text = """
        Experienced Data Scientist skilled in Python, Scikit-learn, SQL, Docker, and Machine Learning.
        Great communication and teamwork skills. Built models using Pandas and NumPy.
        """
        result = analyze_keywords(sample_text)
        self.assertIn('Python', result.technical_skills)
        self.assertIn('Scikit-Learn', result.technical_skills)
        self.assertIn('Sql', [s.title() for s in result.technical_skills])
        self.assertIn('Communication', result.soft_skills)
        self.assertIn('Docker', result.all_keywords)
        self.assertGreater(result.keyword_score, 40)

    def test_score_calculation(self):
        res = calculate_ats_score(
            text_score=90.0,
            structure_score=85.0,
            formatting_score=80.0,
            keyword_score=75.0,
            contact_score=100.0,
        )
        self.assertGreaterEqual(res['score'], 80)
        self.assertLessEqual(res['score'], 90)
        self.assertEqual(res['level'], 'good')
        self.assertIn('Good compatibility', res['category_label'])

    def test_contact_extraction(self):
        text = "Jane Doe\njane.doe@example.com\n+1 555-0199\nlinkedin.com/in/janedoe"
        info = extract_contact_info(text)
        self.assertEqual(info.email, 'jane.doe@example.com')
        self.assertIn('linkedin.com/in/janedoe', info.linkedin)
