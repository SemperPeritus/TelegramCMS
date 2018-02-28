from django.http import HttpResponse

from bots import tasks


def index(request):
    result = tasks.add.delay(2, 3)
    return HttpResponse("Task info: " +
                        str(result.ready()) + " " +
                        str(result.get(timeout=1)) + " " +
                        str(result.ready()))
