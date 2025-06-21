from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
from django.db.models import Avg, Count
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .serializers import *
from .models import *
from datetime import datetime, timedelta, time

# Create your views here.

class EventView(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    # endpoint to add a user to an event
    @action(detail=True, methods=['post'], url_path='add_attendee')
    def add_attendee(self, request, pk=None):
        event = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, id=user_id)
        overlapping = Event.objects.filter(attendees=user, start_time__lt=event.end_time, end_time__gt=event.start_time).exclude(id=event.id)
        
        if overlapping.exists():
            return Response({'error': 'User is already booked for another event at this time'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            event.attendees.add(user)
            return Response({'message': f'User {user.username} added to event: {event.title}'}, status=status.HTTP_200_OK)
        
    # endpoint to remove an attendee from an event
    @action(detail=True, methods=['delete'], url_path='remove_attendee')
    def remove_attendee(self, request, pk=None):
        event = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({'error': 'user_id is missing'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, id=user_id)
        if not event.attendees.filter(id=user_id).exists():
            return Response({'error': f'User {user.username} is not an attendee of the event'}, status=status.HTTP_400_BAD_REQUEST)
        event.attendees.remove(user)
        return Response({'message': f'User: {user.username} removed from the event: {event.title}'})
    
    # endpoint to get available time slots in a given date
    @action(detail=False, methods=['get'], url_path='availability')
    def available_time_slots(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({'error': 'date is a required parameter'})
        try:
            date = parse_date(date_str)
            if date is None:
                raise ValueError()
        except ValueError:
            return Response({'error': 'Invalid date format (expected YYYY-MM-DD)'})
        
        start_of_day = time(9, 0)
        end_of_day = time(21, 0)
        slot_duration = timedelta(hours=1)

        slots = []
        current_time = datetime.combine(date, start_of_day)
        end_time = datetime.combine(date, end_of_day)

        while current_time + slot_duration <= end_time:
            slots.append((current_time.time(), (current_time + slot_duration).time()))
            current_time += slot_duration
        
        conflicts = Event.objects.filter(date=date).values('start_time', 'end_time')        

        available_slots = []
        for start, end in slots:
            conflict_exists = any(
                not (end < c['start_time'] or start > c['end_time']) for c in conflicts
            )
            if not conflict_exists:
                available_slots.append({'start_time': start.strftime('%H:%M'), 'end_time': end.strftime('%H:%M')})
        
        return Response({'date': date_str, 'available_slots': available_slots})

    # endpoint to get analytics of events
    @action(detail=False, methods=['get'], url_path='analytics')
    def analytics(self, request):
        avg_attendance = Event.objects.annotate(num_attendees=Count('attendees')).aggregate(Avg('num_attendees'))
        popular_event_times = Event.objects.values('start_time').annotate(count=Count('id')).order_by('-count')[:3]
        for event in popular_event_times:
            event['start_time'] = event['start_time'].strftime("%H:%M")
            
        return Response({'average_attendance': round(avg_attendance.get('num_attendees__avg', 0), 2), 'popular_start_times': popular_event_times})
    
    # endpoint to search for events based on either title, date or attendees
    @action(detail=False, methods=['get'], url_path='search')
    def search_events(self, request):
        title = request.query_params.get('title')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        attendee_id = request.query_params.get('attendee_id')

        if title:
            queryset = Event.objects.filter(title__icontains=title)

        if start_date and end_date:
            try:
                start, end = parse_date(start_date), parse_date(end_date)
                if start and end:
                    queryset = Event.objects.filter(date__range=(start, end))
            except ValueError:
                return Response({"error": "Invalid date format. (Expected YYYY-MM-DD)"})
            
        if attendee_id:
            queryset = Event.objects.filter(attendees__id=attendee_id)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
