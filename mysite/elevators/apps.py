from django.apps import AppConfig
from .elevator_system import ElevatorSystem


class ElevatorsConfig(AppConfig):
    name = 'elevators'
    es = ElevatorSystem(floor_count=50, elevator_count=4)
