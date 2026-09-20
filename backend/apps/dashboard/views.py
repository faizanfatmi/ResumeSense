from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Count
from apps.documents.models import UploadedFile
from apps.analysis.models import Analysis, Finding
from apps.jobmatcher.models import JobMatch


class DashboardStatsView(APIView):
    """Provides high-level dashboard metrics and recent activity for the user."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        user_analyses = Analysis.objects.filter(uploaded_file__user=user)
        files_count = UploadedFile.objects.filter(user=user).count()

        avg_score_data = user_analyses.aggregate(avg=Avg('score'))
        avg_score = round(avg_score_data['avg'], 1) if avg_score_data['avg'] is not None else 0

        job_matches_count = JobMatch.objects.filter(user=user).count()

        # Count improvement recommendations (critical + important + suggestion)
        improvements_count = Finding.objects.filter(
            analysis__uploaded_file__user=user,
            severity__in=['critical', 'important', 'suggestion']
        ).count()

        # Recent analyses table data
        recent_list = []
        for an in user_analyses.select_related('uploaded_file').order_by('-created_at')[:8]:
            recent_list.append({
                'id': an.id,
                'file_id': an.uploaded_file.id,
                'file_name': an.uploaded_file.original_name,
                'file_type': an.uploaded_file.file_type,
                'file_size': an.uploaded_file.size_display,
                'score': an.score,
                'date': an.created_at.strftime('%b %d, %Y'),
                'datetime': an.created_at.isoformat(),
                'status': an.uploaded_file.processing_status,
                'analysis_type': an.analysis_type,
            })

        return Response({
            'stats': {
                'files_analyzed': files_count,
                'average_score': avg_score,
                'job_matches': job_matches_count,
                'improvements_found': improvements_count,
            },
            'recent_analyses': recent_list,
        })
