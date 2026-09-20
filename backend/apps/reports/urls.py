from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReportsListView.as_view(), name='reports-list'),
    path('<int:analysis_id>/download/', views.ReportDownloadByIdView.as_view(), name='report-download'),
]
