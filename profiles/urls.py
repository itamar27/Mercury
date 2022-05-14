from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from rest_framework.urlpatterns import format_suffix_patterns
from profiles import views

router = DefaultRouter()
router.register('researcher', views.ResearcherViewSet)

urlpatterns = [
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls)),
    path('<int:pk>/details/', views.ResearcherDetails.as_view(), name='researcher details'),
]
