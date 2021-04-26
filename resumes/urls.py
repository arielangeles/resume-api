from resumes.views import ResumeAPIView
from django.urls import path, include
from rest_framework import routers

router = routers.SimpleRouter()
router.register('', ResumeAPIView, basename='resumes')

urlpatterns = [
    path(r'', include(router.urls)),
]