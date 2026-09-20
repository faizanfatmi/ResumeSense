from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.core.files.base import ContentFile
from .models import Analysis, Finding
from .serializers import AnalysisDetailSerializer, FindingSerializer
from .services.report_generator import generate_pdf_report
from apps.documents.models import UploadedFile
import logging

logger = logging.getLogger(__name__)


class AnalysisDetailView(generics.RetrieveAPIView):
    """Retrieve complete analysis details for a document."""
    serializer_class = AnalysisDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure user can only view their own analyses
        return Analysis.objects.filter(uploaded_file__user=self.request.user)


class AnalysisFeedbackView(APIView):
    """Retrieve categorized feedback for an analysis."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            analysis = Analysis.objects.get(pk=pk, uploaded_file__user=request.user)
        except Analysis.DoesNotExist:
            return Response({'error': 'Analysis not found.'}, status=status.HTTP_404_NOT_FOUND)

        severity_filter = request.query_params.get('severity')
        findings_qs = analysis.findings.all()
        if severity_filter and severity_filter != 'all':
            findings_qs = findings_qs.filter(severity=severity_filter)

        serialized = FindingSerializer(findings_qs, many=True).data

        all_findings = analysis.findings.all()
        counts = {
            'all': all_findings.count(),
            'critical': all_findings.filter(severity='critical').count(),
            'important': all_findings.filter(severity='important').count(),
            'suggestion': all_findings.filter(severity='suggestion').count(),
            'good': all_findings.filter(severity='good').count(),
        }

        return Response({
            'analysis_id': analysis.id,
            'counts': counts,
            'findings': serialized,
        })


class AnalysisTextView(APIView):
    """Retrieve extracted text from an analysis."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            analysis = Analysis.objects.get(pk=pk, uploaded_file__user=request.user)
        except Analysis.DoesNotExist:
            return Response({'error': 'Analysis not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'analysis_id': analysis.id,
            'file_name': analysis.uploaded_file.original_name,
            'word_count': analysis.word_count,
            'page_count': analysis.page_count,
            'extracted_text': analysis.extracted_text,
        })


class AnalysisReportDownloadView(APIView):
    """Download analysis report as a formatted PDF."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            analysis = Analysis.objects.get(pk=pk, uploaded_file__user=request.user)
        except Analysis.DoesNotExist:
            return Response({'error': 'Analysis not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            pdf_buffer = generate_pdf_report(analysis)
            filename = f"ResumeSense_Report_{analysis.uploaded_file.original_name}.pdf"

            response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        except Exception as e:
            logger.error(f"Error generating PDF report: {e}", exc_info=True)
            return Response(
                {'error': f'Failed to generate report: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SampleAnalysisCreateView(APIView):
    """
    Creates or returns a high-fidelity sample analysis (matching the user's reference UI).
    Allows instant testing via 'Try Sample' button.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Dynamic candidate name
        display_name = "Candidate"
        try:
            if hasattr(user, 'profile') and user.profile and user.profile.display_name:
                display_name = user.profile.display_name.strip()
        except Exception:
            pass
        if not display_name or display_name == "Candidate":
            display_name = user.get_full_name().strip() or user.username or "Candidate"

        clean_slug = "".join(c for c in display_name if c.isalnum() or c in (' ', '_', '-')).replace(' ', '_')
        file_name = f"{clean_slug or 'Resume'}_Resume.pdf"
        candidate_email = user.email or f"{user.username}@example.com"
        candidate_upper = display_name.upper()

        # Create or fetch demo uploaded file
        demo_file, _ = UploadedFile.objects.get_or_create(
            user=user,
            original_name=file_name,
            defaults={
                'file_type': 'PDF',
                'file_size': 142850,
                'mime_type': 'application/pdf',
                'processing_status': 'COMPLETED',
            }
        )

        if not demo_file.file:
            demo_file.file.save(file_name, ContentFile(b"%PDF-1.4 demo content"), save=True)

        # Create or update sample analysis matching user mockup (Score: 87/100)
        analysis, created = Analysis.objects.get_or_create(
            uploaded_file=demo_file,
            defaults={
                'analysis_type': 'resume',
                'score': 87.0,
                'text_score': 92.0,
                'structure_score': 85.0,
                'keyword_score': 78.0,
                'formatting_score': 90.0,
                'contact_score': 100.0,
                'page_count': 1,
                'word_count': 385,
                'summary': (
                    "Your resume is well-structured and mostly ATS-friendly. A few improvements "
                    "can make it even stronger. Check the detailed feedback for suggestions."
                ),
                'extracted_text': (
                    f"{candidate_upper}\n"
                    "Software Engineer & Data Specialist\n"
                    f"{candidate_email} | +1 (555) 019-2834\n\n"
                    "PROFESSIONAL SUMMARY\n"
                    "Proactive and detail-oriented technical professional passionate about machine learning, "
                    "natural language processing, and cloud architectures. Proven ability to build robust data pipelines "
                    "and full-stack analytical applications.\n\n"
                    "TECHNICAL SKILLS\n"
                    "Languages: Python, SQL, C++, JavaScript\n"
                    "Frameworks & Libraries: Scikit-learn, Pandas, NumPy, Django, React, TensorFlow\n"
                    "Tools: Git, GitHub, Docker, Postman, Linux\n\n"
                    "PROJECTS\n"
                    "ResumeSense — ATS Resume & Presentation Analyzer\n"
                    "• Architected full-stack ATS compatibility platform using Django REST Framework and React.\n"
                    "• Implemented NLP text extraction pipelines for PDF, DOCX, and PPTX formats.\n"
                    "• Evaluated keyword coverage against job descriptions using vector embeddings.\n\n"
                    "Heart Disease Risk Prediction System\n"
                    "• Developed supervised machine learning models achieving 89% classification accuracy.\n"
                    "• Cleaned and preprocessed complex clinical datasets using Pandas and NumPy.\n\n"
                    "EDUCATION\n"
                    "Bachelor of Technology in Computer Science & Engineering\n"
                    "CGPA: 8.7 / 10.0 | Expected Graduation: 2026\n"
                )
            }
        )

        # Populate findings if new
        if created or analysis.findings.count() == 0:
            analysis.findings.all().delete()
            sample_findings = [
                Finding(
                    analysis=analysis,
                    severity='critical',
                    category='keywords',
                    title='Missing Important Keywords',
                    description='Add relevant keywords like "Machine Learning", "Scikit-learn", "SQL" based on your target role.',
                    recommendation='Incorporate target technical competencies in bullet points and skills overview.',
                ),
                Finding(
                    analysis=analysis,
                    severity='important',
                    category='section_structure',
                    title='Improve Section Headings',
                    description='Use standard headings like Experience, Education, Skills, Projects for better ATS parsing.',
                    recommendation='Ensure all section headings use standardized uppercase or title case phrasing.',
                ),
                Finding(
                    analysis=analysis,
                    severity='suggestion',
                    category='formatting',
                    title='Use Standard Fonts',
                    description='Use common fonts like Arial, Calibri, or Times New Roman.',
                    recommendation='Standard typography prevents character encoding distortion in older enterprise parsers.',
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
                    description='Your skills section is clear and well-structured.',
                    recommendation='',
                ),
                Finding(
                    analysis=analysis,
                    severity='good',
                    category='formatting',
                    title='No Images in Important Sections',
                    description='Good! Your resume uses native text instead of embedded images.',
                    recommendation='',
                ),
            ]
            Finding.objects.bulk_create(sample_findings)

        return Response({
            'analysis_id': analysis.id,
            'message': 'Sample analysis ready.',
        }, status=status.HTTP_200_OK)
