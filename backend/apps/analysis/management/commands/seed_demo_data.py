"""
Seed demo data matching the exact UI reference for ResumeSense.
Populates:
- User: Faizan Fatmi (faizan@example.com)
- Profile with avatar and display name
- Uploaded Resume: Faizan_Resume.pdf
- Complete ATS analysis with 87% score, breakdown, findings, and extracted text
- Sample Job Description Match (78% score)
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from apps.accounts.models import UserProfile
from apps.documents.models import UploadedFile
from apps.analysis.models import (
    Analysis, Finding, ExtractedSection, KeywordGroup, SlideAnalysis
)
from apps.jobmatcher.models import JobDescription, JobMatch


class Command(BaseCommand):
    help = 'Seeds high-fidelity demo data for ResumeSense'

    def handle(self, *args, **options):
        self.stdout.write("Seeding demo data...")

        # 1. Create or get user
        user, created = User.objects.get_or_create(
            username='faizan',
            defaults={
                'email': 'faizan@example.com',
                'first_name': 'Faizan',
                'last_name': 'Fatmi',
            }
        )
        user.set_password('ResumeSense123!')
        user.save()

        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={'display_name': 'Faizan Fatmi'}
        )

        # 2. Uploaded file
        resume_file, _ = UploadedFile.objects.get_or_create(
            user=user,
            original_name='Faizan_Resume.pdf',
            defaults={
                'file_type': 'PDF',
                'file_size': 245760,
                'mime_type': 'application/pdf',
                'processing_status': 'COMPLETED',
            }
        )
        if not resume_file.file:
            resume_file.file.save("Faizan_Resume.pdf", ContentFile(b"%PDF-1.4 demo file content"), save=True)

        # Also create a sample PPTX file
        ppt_file, _ = UploadedFile.objects.get_or_create(
            user=user,
            original_name='Data_Science_Project_Overview.pptx',
            defaults={
                'file_type': 'PPTX',
                'file_size': 1843200,
                'mime_type': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'processing_status': 'COMPLETED',
            }
        )
        if not ppt_file.file:
            ppt_file.file.save("Data_Science_Project_Overview.pptx", ContentFile(b"PK demo pptx content"), save=True)

        # 3. Create Resume Analysis (Score: 87/100, exactly matching reference mockup)
        resume_file.analyses.all().delete()
        analysis = Analysis.objects.create(
            uploaded_file=resume_file,
            analysis_type='resume',
            score=87.0,
            text_score=92.0,
            structure_score=85.0,
            keyword_score=78.0,
            formatting_score=90.0,
            contact_score=100.0,
            page_count=1,
            word_count=420,
            processing_time=1.42,
            summary=(
                "Your resume is well-structured and mostly ATS-friendly. A few improvements "
                "can make it even stronger. Check the detailed feedback for suggestions."
            ),
            extracted_text=(
                "FAIZAN FATMI\n"
                "Data Science Student\n"
                "faizan@example.com | +91 98765 43210 | Durgapur, India\n"
                "linkedin.com/in/faizanfatmi | github.com/faizanfatmi\n\n"
                "PROFESSIONAL SUMMARY\n"
                "Detail-driven Data Science student with a strong foundation in predictive modeling, "
                "machine learning pipelines, and full-stack software architecture. Proficient in Python, "
                "SQL, and modern data processing libraries. Passionate about applying AI to real-world products.\n\n"
                "TECHNICAL SKILLS\n"
                "Languages: Python, SQL, C++, JavaScript, TypeScript\n"
                "Frameworks & Libraries: Scikit-learn, Pandas, NumPy, Django, React, PyTorch\n"
                "Tools & Platforms: Git, GitHub, Docker, Postman, Linux, PostgreSQL, VS Code\n\n"
                "EXPERIENCE & PROJECTS\n"
                "ResumeSense — Professional ATS Resume & PPT Analyzer\n"
                "• Engineered end-to-end multi-format document parsing engine supporting PDF, DOCX, and PPTX.\n"
                "• Designed ATS compatibility heuristic evaluator scoring structure, formatting, and keyword density.\n"
                "• Built semantic job matcher calculating cosine similarity between job descriptions and resumes.\n\n"
                "Heart Disease Risk Classification Platform\n"
                "• Developed ensemble classification models achieving 91.2% ROC-AUC on clinical trial datasets.\n"
                "• Performed exploratory data analysis, outlier remediation, and feature importance analysis.\n\n"
                "EDUCATION\n"
                "Bachelor of Technology in Computer Science and Engineering\n"
                "National Institute of Technology | CGPA: 8.7 / 10.0 | 2022 – 2026\n"
            )
        )

        # 4. Create Findings matching the reference screenshot
        findings = [
            Finding(
                analysis=analysis,
                severity='critical',
                category='keywords',
                title='Missing Important Keywords',
                description='Add relevant keywords like "Machine Learning", "Scikit-learn", "SQL" based on your target role.',
                recommendation='Add explicit keyword mentions in your project bullet points and skills overview.',
            ),
            Finding(
                analysis=analysis,
                severity='critical',
                category='section_structure',
                title='Quantify Work Impact Metrics',
                description='2 project descriptions lack measurable business or statistical outcomes.',
                recommendation='Include percentages, processing speeds, or data volumes to prove quantifiable impact.',
            ),
            Finding(
                analysis=analysis,
                severity='important',
                category='section_structure',
                title='Improve Section Headings',
                description='Use standard headings like Experience, Education, Skills, Projects for better ATS parsing.',
                recommendation='Ensure all section headers conform to standard capitalization and recognized keywords.',
            ),
            Finding(
                analysis=analysis,
                severity='important',
                category='keywords',
                title='Cloud Platform Coverage',
                description='No specific cloud vendors (AWS, GCP, Azure) detected in technical competencies.',
                recommendation='If experienced with cloud deployment, add AWS, GCP, or Azure explicitly.',
            ),
            Finding(
                analysis=analysis,
                severity='important',
                category='formatting',
                title='Bullet Point Density',
                description='A few bullet points extend beyond three lines of text, which may slow ATS parsing.',
                recommendation='Keep bullet points concise (1 to 2 lines) with an active action verb at the start.',
            ),
            Finding(
                analysis=analysis,
                severity='suggestion',
                category='formatting',
                title='Use Standard Fonts',
                description='Use common fonts like Arial, Calibri, or Times New Roman.',
                recommendation='Standard typography guarantees compatibility across legacy Applicant Tracking Systems.',
            ),
            Finding(
                analysis=analysis,
                severity='suggestion',
                category='layout',
                title='Hyperlink Presentation',
                description='Raw URL links were found. Use descriptive link labels where supported.',
                recommendation='Format links cleanly without extraneous URL query tracking parameters.',
            ),
            Finding(
                analysis=analysis,
                severity='good',
                category='contact_info',
                title='Contact Information Detected',
                description='Your name, email, and phone number were successfully detected.',
                recommendation='',
            ),
            Finding(
                analysis=analysis,
                severity='good',
                category='section_structure',
                title='Skills Section Detected',
                description='Your skills section is clear and well structured.',
                recommendation='',
            ),
            Finding(
                analysis=analysis,
                severity='good',
                category='formatting',
                title='No Images in Important Sections',
                description='Good! Your resume uses native text instead of images.',
                recommendation='',
            ),
            Finding(
                analysis=analysis,
                severity='good',
                category='section_structure',
                title='Standard Education Format',
                description='Degree, institution name, graduation year, and GPA are clearly defined.',
                recommendation='',
            ),
            Finding(
                analysis=analysis,
                severity='good',
                category='formatting',
                title='Clean Single-Page Length',
                description='Document fits cleanly within standard 1-page limits for early-career professionals.',
                recommendation='',
            ),
        ]
        Finding.objects.bulk_create(findings)

        # 5. Extracted Sections
        sections = [
            ExtractedSection(analysis=analysis, section_name='Contact Information', content='faizan@example.com | +91 98765 43210', detected=True, confidence=1.0, order=0),
            ExtractedSection(analysis=analysis, section_name='Summary', content='Detail-driven Data Science student...', detected=True, confidence=0.95, order=1),
            ExtractedSection(analysis=analysis, section_name='Technical Skills', content='Python, SQL, React, Django...', detected=True, confidence=0.98, order=2),
            ExtractedSection(analysis=analysis, section_name='Projects', content='ResumeSense, Heart Disease Platform...', detected=True, confidence=0.96, order=3),
            ExtractedSection(analysis=analysis, section_name='Education', content='B.Tech in Computer Science...', detected=True, confidence=0.99, order=4),
        ]
        ExtractedSection.objects.bulk_create(sections)

        # 6. Keyword Groups
        KeywordGroup.objects.create(
            analysis=analysis,
            group_name='Technical Skills',
            keywords=['Python', 'SQL', 'Scikit-learn', 'Pandas', 'NumPy', 'Django', 'React', 'PyTorch', 'C++', 'JavaScript']
        )
        KeywordGroup.objects.create(
            analysis=analysis,
            group_name='Tools & Platforms',
            keywords=['Git', 'GitHub', 'Docker', 'Postman', 'Linux', 'PostgreSQL', 'VS Code']
        )
        KeywordGroup.objects.create(
            analysis=analysis,
            group_name='Soft Skills',
            keywords=['Problem Solving', 'Teamwork', 'Communication', 'Attention to Detail']
        )

        # 7. Create PPT Analysis
        ppt_file.analyses.all().delete()
        ppt_analysis = Analysis.objects.create(
            uploaded_file=ppt_file,
            analysis_type='ppt',
            score=72.0,
            text_score=78.0,
            structure_score=70.0,
            keyword_score=75.0,
            formatting_score=68.0,
            contact_score=65.0,
            page_count=4,
            word_count=210,
            processing_time=0.88,
            summary="Presentation Analysis: 4 slides analyzed. 1 slide contains text inside embedded image. Moderate text density.",
            extracted_text="Slide 1: Data Science Project Overview\nSlide 2: Architecture\nSlide 3: Pipeline & Results\nSlide 4: Conclusion"
        )
        SlideAnalysis.objects.create(analysis=ppt_analysis, slide_number=1, extracted_text='Project Overview and Goals', text_quality='good', has_images=False, has_tables=False)
        SlideAnalysis.objects.create(analysis=ppt_analysis, slide_number=2, extracted_text='Architecture Diagram', text_quality='poor', has_images=True, has_tables=False, warnings=['Important skills appear inside an image'])
        SlideAnalysis.objects.create(analysis=ppt_analysis, slide_number=3, extracted_text='Evaluation Metrics & Models', text_quality='warning', has_images=False, has_tables=True, warnings=['Text size may be difficult to parse (9pt detected)'])
        SlideAnalysis.objects.create(analysis=ppt_analysis, slide_number=4, extracted_text='Summary and Next Steps', text_quality='good', has_images=False, has_tables=False)

        # 8. Sample Job Match (Score: 78/100, exactly matching reference mockup)
        jd_content = (
            "We are looking for a Data Scientist with experience in Python, Machine Learning, "
            "SQL, and data visualization. The ideal candidate should have experience with "
            "scikit-learn, deep learning, and data analysis. Experience with model deployment, "
            "Pandas, and NumPy is strongly preferred."
        )
        jd = JobDescription.objects.create(
            user=user,
            title='Data Scientist Role',
            content=jd_content,
        )

        JobMatch.objects.create(
            user=user,
            analysis=analysis,
            job_description=jd,
            match_score=78.0,
            matched_keywords=['Python', 'Pandas', 'NumPy', 'Machine Learning', 'Data Analysis'],
            missing_keywords=['Scikit-learn', 'SQL (add more details)', 'Data Visualization', 'Deep Learning', 'Model Deployment'],
            suggestions=[
                "If you genuinely have experience with SQL, consider making it more visible in your Skills or Project sections.",
                "Mention specific Data Visualization packages (e.g., Matplotlib, Seaborn) if you have utilized them in your coursework or projects.",
                "Highlight deep learning architectures or neural networks if you have worked with PyTorch or TensorFlow."
            ]
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded demo data for ResumeSense!"))
