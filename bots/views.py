from celery.result import AsyncResult
from django.http import HttpResponse


def index(request):
    task = AsyncResult(id='1c7838c7-98fc-48db-b72e-20ff3bd6009e')
    return HttpResponse(str(task.ready()) + " " + str(task.get()))
