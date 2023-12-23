import subprocess
from wsgiref.util import FileWrapper

from django.http import HttpResponse
from django.views.decorators.http import require_GET
from rest_framework import viewsets

from .models import Text
from .serializers import TextSerializer


@require_GET
def runtext(request):
    text = request.GET.get("text", None)
    if text is not None:
        new_text = Text(text=text)
        new_text.save()
    else:
        text = "Here could be your text"

    # generate_running_text_video(text, "runtext_video.avi")
    process = subprocess.Popen(("python", "main/runtext.py", f"{text}"))
    process.wait()
    video = FileWrapper(open("voiced_running_text_video.avi", "rb"))

    response = HttpResponse(video, content_type="video/avi")
    response["Content-Disposition"] = "attachment; filename=runtext_video.avi"
    return response


class TextView(viewsets.ModelViewSet):
    queryset = Text.objects.order_by("-get_time")
    serializer_class = TextSerializer
