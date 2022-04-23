from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from research import views

urlpatterns = [
    path('<int:researchId>/participants/', views.ParticipantList.as_view(), name="participants"),
    path('<int:researchId>/participants/<int:pk>', views.ParticipantDetails.as_view(), name="participant"),
    path('<int:researchId>/interactions/', views.InteractionList.as_view(), name="interaction"),
    path('<int:researchId>/interactions/network',views.InteractionsNetworkAPIView.as_view(), name="interaction network view"),
    path('<int:researchId>/gameConfiguration', views.GameConfigurationDetail.as_view(), name='game configuration'),
]
