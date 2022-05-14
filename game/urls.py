from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from game import views

urlpatterns = [
    path('player/', views.PlayerDetail.as_view(), name="player"),
    path('configuration/', views.GameConfigurationDetail.as_view(), name="configuration"),
    path('interaction/', views.InteractionDetail.as_view(), name="interaction"),
    path('player/<int:pk>/update/', views.PlayerDetail.as_view(), name="player update")
]
