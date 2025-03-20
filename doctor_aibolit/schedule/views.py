from django.http import Http404
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from schedule.models import Schedule
from schedule.serializers import ScheduleSerializer
from schedule.services import create_pill_schedule, get_time_next_pills


class ScheduleViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        id_schedule: int = response.data['id']
        response.data.clear()
        response.data['id'] = id_schedule
        return response

    def list(*args, **kwargs):
        queryset = Schedule.objects.filter(user_id=kwargs['user_id']).values_list('id')
        return Response([i[0] for i in queryset])

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        if kwargs['user_id'] != response.data['user_id']:
            raise Http404('detail": "No Schedule matches the given query.')
        pill_schedule = create_pill_schedule(response.data['periodicity'])
        response.data['pill_schedule'] = {num: str(time) for num, time in enumerate(pill_schedule, start=1)}
        return response


class PillApiView(APIView):

    def get(self, request, *args, **kwargs):
        queryset = Schedule.objects.filter(user_id=kwargs['user_id']).values('name_medicine', 'periodicity')
        time_next_pills: list[dict[str, list[str]]] = []
        for obj in queryset:
            next_takings = get_time_next_pills(obj['periodicity'])
            if next_takings:
                time_next_pills.append({obj['name_medicine']: next_takings})
        return Response(time_next_pills)