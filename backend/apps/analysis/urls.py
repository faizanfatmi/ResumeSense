from django.urls import path
from . import views

urlpatterns = [
    path('sample/', views.SampleAnalysisCreateView.as_view(), name='analysis-sample'),
    path('<int:pk>/', views.AnalysisDetailView.as_view(), name='analysis-detail'),
    path('<int:pk>/feedback/', views.AnalysisFeedbackView.as_view(), name='analysis-feedback'),
    path('<int:pk>/text/', views.AnalysisTextView.as_view(), name='analysis-text'),
    path('<int:pk>/report/', views.AnalysisReportDownloadView.as_view(), name='analysis-report'),
]
