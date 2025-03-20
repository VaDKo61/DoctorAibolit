from django.urls import path

from schedule.views import ScheduleViewSet, PillApiView

urlpatterns = [
    path('schedule', ScheduleViewSet.as_view({'post': 'create'})),
    path('schedules/user_id=<int:user_id>', ScheduleViewSet.as_view({'get': 'list'})),
    path('schedule/user_id=<int:user_id>&schedule_id=<pk>', ScheduleViewSet.as_view({'get': 'retrieve'})),
    path('next_takings/user_id=<int:user_id>', PillApiView.as_view()),
]
