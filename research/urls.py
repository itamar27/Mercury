from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from research import views

urlpatterns = [
    path('', views.ResearchApiViewList.as_view(), name="research"),
    path('<int:researchId>/details', views.ResearchApiViewDetail.as_view(), name="research detail"),
    path('participants/', views.ParticipantList.as_view(), name="participants"),
    path('participants/<int:pk>/', views.ParticipantDetails.as_view(), name="participant detail"),
    path('interactions/', views.InteractionList.as_view(), name="interaction"),
    path('interactions/network',views.InteractionsNetworkAPIView.as_view(), name="interaction network view"),
    path('gameConfiguration', views.GameConfigurationDetail.as_view(), name='game configuration'),
]
