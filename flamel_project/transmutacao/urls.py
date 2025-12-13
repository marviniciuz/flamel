# flamel_project/transmutacao/urls.py

from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.dashboard_view, name='dashboard'),

    # 1. Login (Simulação)
    path('login/', views.login_mock_view, name='login'), 
    
    # 3. ENDPOINT DE UPLOAD (SOLUÇÃO DO ERRO)
    path('upload/', views.upload_file_view, name='upload_file'),
    
    # 4. ENDPOINT DE STATUS (Para o polling do Celery/HTMX)
    path('status/<str:task_id>/', views.task_status_view, name='task_status'),
    
    # 5. ENDPOINT DE DOWNLOAD
    path('download/<int:file_id>/', views.download_file_view, name='download_file'),
]
