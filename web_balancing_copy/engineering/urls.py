from django.urls import path
from . import views

urlpatterns = [
    path('update_sah_by_operation/', views.update_sah_by_operation, name='update_sah'),
    path('engineering/', views.engineering, name='engineering'),
]