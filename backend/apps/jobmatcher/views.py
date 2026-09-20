from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import JobDescription, JobMatch
from .serializers import JobMatchSerializer, MatchRequestSerializer
from .services.job_matcher import match_resume_to_job
from apps.analysis.models import Analysis
import logging

logger = logging.getLogger(__name__)


class RunJobMatchView(APIView):
    """Compare a resume against a target job description."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MatchRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        analysis_id = serializer.validated_data.get('analysis_id')
        jd_text = serializer.validated_data['job_description']
        title = serializer.validated_data.get('title', 'Target Role')

        # Find target analysis
        if analysis_id:
            try:
                analysis = Analysis.objects.get(pk=analysis_id, uploaded_file__user=user)
            except Analysis.DoesNotExist:
                return Response(
                    {'error': 'Selected analysis not found or does not belong to you.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Pick latest resume analysis for user
            analysis = Analysis.objects.filter(
                uploaded_file__user=user,
                analysis_type='resume'
            ).order_by('-created_at').first() or Analysis.objects.filter(
                uploaded_file__user=user
            ).order_by('-created_at').first()
            if not analysis:
                return Response(
                    {'error': 'No analyzed resumes found. Please upload a resume first.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Store Job Description
        jd_obj = JobDescription.objects.create(
            user=user,
            title=title,
            content=jd_text
        )

        # Perform matching
        match_result = match_resume_to_job(
            resume_text=analysis.extracted_text,
            job_description=jd_text
        )

        # Save JobMatch record
        job_match = JobMatch.objects.create(
            user=user,
            analysis=analysis,
            job_description=jd_obj,
            match_score=match_result.match_score,
            matched_keywords=match_result.matched_skills,
            missing_keywords=match_result.missing_skills,
            suggestions=match_result.suggestions,
        )

        return Response(JobMatchSerializer(job_match).data, status=status.HTTP_201_CREATED)


class JobMatchHistoryView(generics.ListAPIView):
    """List recent job matches for the authenticated user."""
    serializer_class = JobMatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobMatch.objects.filter(user=self.request.user)


class JobMatchDetailView(generics.RetrieveAPIView):
    """Get single job match details."""
    serializer_class = JobMatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobMatch.objects.filter(user=self.request.user)
