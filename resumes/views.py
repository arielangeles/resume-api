from rest_framework.response import Response
from resumes.serializers import BasicSerializer, ProfileSerializer, ResumeSerializer
from resumes.models import Basic, Resume
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_condition import etag
from resumes.utils import check_etag, custom_etag, custom_update

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

    @etag(custom_etag)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @etag(custom_etag)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer
        return custom_update(request, instance, serializer, partial)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=['GET', 'PUT'])
    def basics(self, request, basics__name):
        basic = Basic.objects.get(name=basics__name)

        if request.method == 'GET':
            check_etag(
                basic.resume, 
                [basic], 
                ('name', 'label', 'picture', 'email', 'phone', 'website', 'summary', 'location_id')
            )

            serializer = BasicSerializer(instance=basic)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            return custom_update(request, basic, BasicSerializer)


    @action(detail=True, methods=['GET', 'POST'], url_path='basics/profiles')
    def profiles(self, request, basics__name):
        basic = Basic.objects.get(name=basics__name)
        profiles = basic.profiles.all()

        check_etag(basic.resume, profiles, ('network', 'username', 'url'))

        if request.method == 'GET':
            serializer = ProfileSerializer(profiles, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = ProfileSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(basic_id=basic.id)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        elif request.method == 'PUT':
            return custom_update(request, basic, BasicSerializer)