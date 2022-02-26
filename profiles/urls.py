from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from profiles import views


urlpatterns = [
    path('researchers/', views.ResearcherListApiView.as_view()),
    path('researchers/<int:pk>/', views.ResearcherDetailApiView.as_view()),
    path('participants/', views.ParticipantListApiView.as_view()),
    path('participants/<int:pk>/', views.ParticipantDetailApiView.as_view()),  
    # path('login/', views.UserLoginApiView.as_view()),    
]


urlpatterns = format_suffix_patterns(urlpatterns)
