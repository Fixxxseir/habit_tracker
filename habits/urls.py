from django.urls import include, path
from rest_framework import routers

from habits import views
from habits.apps import HabitConfig

app_name = HabitConfig.name


router = routers.DefaultRouter()

router.register(prefix=r'habit', viewset=views.HabitViewSet, basename="habit")

urlpatterns = [
    path('', include(router.urls))
]
