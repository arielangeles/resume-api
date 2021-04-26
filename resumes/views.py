import hashlib

from rest_framework.response import Response
from resumes.serializers import BasicSerializer, ProfileSerializer, ResumeSerializer
from resumes.models import Basic, Resume
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_condition import etag


def custom_etag(request, *args, **kwargs):
    path = request.META.get('PATH_INFO')  # type: str
    name = path.split('/')[-2]
    try:
        resume = Resume.objects.get(basics__name=name)
        version = resume.version  # instance version
    except (Resume.DoesNotExist, AttributeError):
        version = Resume.objects.last().pk  # new resource

    return hashlib.md5((str(version)).encode('utf-8')).hexdigest()

class ResumeAPIView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    lookup_field = 'basics__name'
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @etag(custom_etag)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def basics(self, request, basics__name):
        basic = Basic.objects.get(name=basics__name)

        serializer = BasicSerializer(instance=basic)

        return Response(serializer.data)

    @action(detail=True, methods=['GET', 'POST'], url_path='basics/profiles')
    def profiles(self, request, basics__name):
        basic = Basic.objects.get(name=basics__name)
        if request.method == 'GET':
            profiles = basic.profiles.all()
            serializer = ProfileSerializer(profiles, many=True)

            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = ProfileSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(basic_id=basic.id)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    