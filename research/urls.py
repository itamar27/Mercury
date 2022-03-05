from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from research import views

urlpatterns = [
    path('participants/', views.ParticipantList.as_view(), name="participants")
]
