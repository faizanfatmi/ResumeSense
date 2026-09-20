from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse
from .models import UploadedFile
from .serializers import UploadedFileSerializer, FileUploadSerializer, FileListSerializer
from .validators import validate_file_type, validate_file_not_empty
import logging

logger = logging.getLogger(__name__)


class FileUploadView(generics.CreateAPIView):
    """Upload a document file for analysis."""
    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data['file']
        analysis_type = serializer.validated_data.get('analysis_type', 'resume')

        # Validate file
        try:
            validate_file_not_empty(file)
            file_type, mime_type = validate_file_type(file)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create UploadedFile record
        uploaded_file = UploadedFile.objects.create(
            user=request.user,
            original_name=file.name,
            file=file,
            file_type=file_type,
            file_size=file.size,
            mime_type=mime_type,
            processing_status=UploadedFile.ProcessingStatus.UPLOADED,
        )

        logger.info(f"File uploaded: {file.name} ({file_type}) by user {request.user.username}")

        # Trigger analysis
        try:
            uploaded_file.processing_status = UploadedFile.ProcessingStatus.PROCESSING
            uploaded_file.save()

            from apps.analysis.services.analysis_pipeline import run_analysis_pipeline
            analysis = run_analysis_pipeline(uploaded_file, analysis_type)

            uploaded_file.processing_status = UploadedFile.ProcessingStatus.COMPLETED
            uploaded_file.save()

            return Response({
                'file': UploadedFileSerializer(uploaded_file).data,
                'analysis_id': analysis.id,
                'message': 'File uploaded and analyzed successfully.'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Analysis failed for {file.name}: {str(e)}", exc_info=True)
            uploaded_file.processing_status = UploadedFile.ProcessingStatus.FAILED
            uploaded_file.error_message = str(e)
            uploaded_file.save()

            return Response({
                'file': UploadedFileSerializer(uploaded_file).data,
                'error': f"File uploaded but analysis failed: {str(e)}"
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class FileListView(generics.ListAPIView):
    """List all files uploaded by the current user."""
    serializer_class = FileListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UploadedFile.objects.filter(user=self.request.user)


class FileDetailView(generics.RetrieveDestroyAPIView):
    """Retrieve or delete a specific file."""
    serializer_class = UploadedFileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UploadedFile.objects.filter(user=self.request.user)


class FileDownloadView(generics.GenericAPIView):
    """Download the original uploaded file."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            uploaded_file = UploadedFile.objects.get(pk=pk, user=request.user)
        except UploadedFile.DoesNotExist:
            return Response(
                {'error': 'File not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        return FileResponse(
            uploaded_file.file.open('rb'),
            as_attachment=True,
            filename=uploaded_file.original_name
        )
