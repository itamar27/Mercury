from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from research import views

urlpatterns = [
    path('participants/', views.ParticipantList.as_view(), name="participants"),
    path('participants/<int:pk>', views.ParticipantDetails.as_view(), name="participant"),
    path('interactions/', views.InteractionAPIView.as_view(), name="interaction"),
    path('interactions/network',views.InteractionsNetworkAPIView.as_view(), name="interaction network view"),
]
