import hashlib

from resumes.models import Resume
from rest_framework.response import Response
from rest_framework import status


def custom_etag(request, *args, **kwargs):
    path = request.META.get('PATH_INFO')  # type: str
    name = path.split('/')[-2]
    try:
        resume = Resume.objects.get(basics__name=name)
        version = resume.version  # instance version
    except (Resume.DoesNotExist, AttributeError):
        version = Resume.objects.last().pk  # new resource

    return hashlib.md5((str(version)).encode('utf-8')).hexdigest()


def track_etag(queryset, tracked_fields):
    for instance in queryset:
        return any(instance.tracker.has_changed(field) for field in tracked_fields)

def check_etag(resume_instance, queryset, tracked_fields):
    resume_instance.version += 1 if track_etag(queryset, tracked_fields) else 0
    resume_instance.save()

def custom_update(request, instance, serializer_class, partial=False):

    if_match = request.headers.get('If-Match')
    etag = custom_etag(request)

    if if_match and if_match != etag:
        response = Response({'Error': 'Someone already updated this resource'}, status=status.HTTP_409_CONFLICT)
        response.headers.setdefault('Etag', etag)
        return response

    serializer = serializer_class(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    response = Response(serializer.data)
    response.headers.setdefault('Etag', etag)

    return response