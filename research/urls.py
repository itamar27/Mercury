from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from research import views

urlpatterns = [
    path('', views.ResearchApiViewList.as_view(), name="research"),
    path('<int:researchId>/details/', views.ResearchApiViewDetail.as_view(), name="research detail"),
    path('<int:researchId>/details/interactions/', views.InteractionsListAPIViw.as_view(), name="research detail"),
    path('<int:researchId>/network/',views.NetworkAPIView.as_view(), name="network view"),
]
