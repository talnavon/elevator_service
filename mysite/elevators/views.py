from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponseBadRequest
from threading import Thread
from .elevator_system import ElevatorSystem


def index(request):

    if request.method == 'POST':
        floor = request.POST.get("floor", "0")
        direction = 1 if int(floor) != 0 else -1
        try:
            elevator = ElevatorSystem.get_instance().call_elevator(floor=int(floor), direction=direction)
            Thread(target=ElevatorSystem.get_instance().move_elevator, args=(elevator, int(floor))).start()
            return JsonResponse({'elevator': str(elevator)})
        except ValueError as ve:
            return HttpResponseBadRequest(str(ve))
        except Exception:
            i = 10
            while i <= int(floor):
                elevator = ElevatorSystem.get_instance().call_elevator(floor=i, direction=direction)
                Thread(target=ElevatorSystem.get_instance().move_elevator, args=(elevator, int(floor))).start()
                i += 10
                return JsonResponse({'elevator': str(elevator)})

    elif request.method == 'GET':
        return JsonResponse({'Welcome to the Elevator system': 'for elevator request : (POST) /getElevator'})

    # return HttpResponse("You got Elevator: ")


class HomePageView(TemplateView):
    template_name = 'home.html'

