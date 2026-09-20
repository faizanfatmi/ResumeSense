from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.FileUploadView.as_view(), name='file-upload'),
    path('', views.FileListView.as_view(), name='file-list'),
    path('<int:pk>/', views.FileDetailView.as_view(), name='file-detail'),
    path('<int:pk>/download/', views.FileDownloadView.as_view(), name='file-download'),
]
