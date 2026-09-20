from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import HttpResponse
from apps.analysis.models import Analysis
from apps.analysis.services.report_generator import generate_pdf_report


class ReportsListView(APIView):
    """Lists all available reports that can be downloaded."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        analyses = Analysis.objects.filter(uploaded_file__user=request.user).select_related('uploaded_file')
        data = []
        for a in analyses:
            data.append({
                'id': a.id,
                'file_name': a.uploaded_file.original_name,
                'score': a.score,
                'date': a.created_at.strftime('%b %d, %Y'),
                'download_url': f'/api/analysis/{a.id}/report/'
            })
        return Response(data)


class ReportDownloadByIdView(APIView):
    """Direct report download endpoint by analysis ID."""
    permission_classes = [IsAuthenticated]

    def get(self, request, analysis_id):
        try:
            analysis = Analysis.objects.get(pk=analysis_id, uploaded_file__user=request.user)
        except Analysis.DoesNotExist:
            return Response({'error': 'Report not found.'}, status=status.HTTP_404_NOT_FOUND)

        pdf_buffer = generate_pdf_report(analysis)
        filename = f"ResumeSense_Report_{analysis.uploaded_file.original_name}.pdf"

        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
