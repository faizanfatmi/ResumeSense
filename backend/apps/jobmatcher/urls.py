from django.urls import path
from . import views

urlpatterns = [
    path('match/', views.RunJobMatchView.as_view(), name='job-match-run'),
    path('history/', views.JobMatchHistoryView.as_view(), name='job-match-history'),
    path('<int:pk>/', views.JobMatchDetailView.as_view(), name='job-match-detail'),
]
