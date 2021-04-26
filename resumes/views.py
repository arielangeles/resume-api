from rest_framework.response import Response
from resumes.serializers import BasicSerializer, ProfileSerializer, ResumeSerializer, VolunteerSerializer, WorkSerializer
from resumes.models import Basic, Profile, Resume, Volunteer, Work
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
        basic = Basic.objects.filter(name=basics__name).last()
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

    @action(detail=True, methods=['PUT', 'DELETE'], url_path='basics/profiles/(?P<network>[\w.@+-]+)')
    def edit_profiles(self, request, basics__name, network):
        basic = Basic.objects.filter(name=basics__name).last()
        profiles = basic.profiles.all()

        check_etag(basic.resume, profiles, ('network', 'username', 'url'))

        instance = Profile.objects.get(network=network)

        if request.method == 'PUT':
            return custom_update(request, instance, ProfileSerializer)

        elif request.method == 'DELETE':
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['GET', 'POST'])
    def work(self, request, basics__name):
        resume = Basic.objects.filter(name=basics__name).last().resume
        work = resume.work.all()

        check_etag(
            resume,
            work,
            ('company', 'position', 'website', 'start_date', 'end_date', 'summary')
        )

        if request.method == 'GET':
            serializer = WorkSerializer(work, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = WorkSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(resume_id=resume.id)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['PUT', 'DELETE'], url_path='work/(?P<company>[\w.@+-]+)')
    def edit_work(self, request, basics__name, company):
        resume = Basic.objects.filter(name=basics__name).last().resume
        work = resume.work.all()

        check_etag(resume, work, ('company', 'position', 'website', 'start_date', 'end_date', 'summary'))

        instance = Work.objects.get(company=company)

        if request.method == 'PUT':
            return custom_update(request, instance, WorkSerializer)

        elif request.method == 'DELETE':
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['GET', 'POST'])
    def volunteer(self, request, basics__name):
        resume = Basic.objects.filter(name=basics__name).last().resume
        volunteer = resume.volunteer.all()

        check_etag(
            resume,
            volunteer,
            ('organization', 'position', 'website', 'start_date', 'end_date', 'summary')
        )

        if request.method == 'GET':
            serializer = VolunteerSerializer(volunteer, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = VolunteerSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(resume_id=resume.id)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['PUT', 'DELETE'], url_path='volunteer/(?P<organization>[\w\ .@+-]+)')
    def edit_volunteer(self, request, basics__name, organization):
        resume = Basic.objects.filter(name=basics__name).last().resume
        volunteer = resume.volunteer.all()

        check_etag(resume, volunteer, ('organization', 'position', 'website', 'start_date', 'end_date', 'summary'))

        instance = Volunteer.objects.get(organization=organization)

        if request.method == 'PUT':
            return custom_update(request, instance, VolunteerSerializer)

        elif request.method == 'DELETE':
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)