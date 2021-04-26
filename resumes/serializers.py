from resumes.models import (
    Award, Basic, Course, Education, Highlight, Interest, Keyword, Language,
    Location, Profile, Publication, Reference, Resume, Skill, Volunteer, Work
)
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer


class LocationSerializer(WritableNestedModelSerializer):
    postalCode = serializers.CharField(source='postal_code')
    countryCode = serializers.CharField(source='country_code')

    class Meta:
        model = Location
        fields = ('address', 'postalCode', 'city', 'countryCode', 'region')


class ProfileSerializer(WritableNestedModelSerializer):

    class Meta:
        model = Profile
        fields = ('network', 'username', 'url')


class BasicSerializer(WritableNestedModelSerializer):
    location = LocationSerializer()
    profiles = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Basic
        fields = ('name', 'label', 'picture', 'email', 'phone', 'website',
                  'summary', 'location', 'profiles')
    
    # def create(self, validated_data):
    #     profiles = validated_data.pop('profiles')

    #     for profile in profiles:
    #         self.instance.profiles.add(profile)
    #         self.instance.save()
        
    #     return super().create(validated_data)


class HighlightSerializer(WritableNestedModelSerializer):

    class Meta:
        model = Highlight
        fields = ('name',)


class CourseSerializer(WritableNestedModelSerializer):

    class Meta:
        model = Course
        fields = ('name',)


class KeywordSerializer(WritableNestedModelSerializer):

    class Meta:
        model = Keyword
        fields = ('name',)


class WorkSerializer(WritableNestedModelSerializer):
    highlights = HighlightSerializer(many=True)
    startDate = serializers.DateField(source='start_date')
    endDate = serializers.DateField(source='end_date')

    class Meta:
        model = Work
        fields = ('company', 'position', 'website', 'startDate', 'endDate',
                  'summary', 'highlights')


class VolunteerSerializer(WritableNestedModelSerializer):
    highlights = HighlightSerializer(many=True)
    startDate = serializers.DateField(source='start_date')
    endDate = serializers.DateField(source='end_date')

    class Meta:
        model = Volunteer
        fields = ('organization', 'position', 'website', 'startDate', 'endDate',
                  'summary', 'highlights')


class EducationSerializer(WritableNestedModelSerializer):
    courses = CourseSerializer(many=True)
    studyType = serializers.CharField(source='study_type')
    startDate = serializers.DateField(source='start_date')
    endDate = serializers.DateField(source='end_date')

    class Meta:
        model = Education
        fields = ('institution', 'area', 'studyType', 'startDate', 'endDate',
                  'gpa', 'courses')


class AwardSerializer(WritableNestedModelSerializer):

    class Meta:
        model = Award
        fields = ('title', 'date', 'awarder', 'summary')


class PublicationSerializer(WritableNestedModelSerializer):
    releaseDate = serializers.DateField(source='release_date')

    class Meta:
        model = Publication
        fields = ('name', 'publisher', 'releaseDate', 'website', 'summary')


class SkillSerializer(WritableNestedModelSerializer):
    keywords = KeywordSerializer(many=True)

    class Meta:
        model = Skill
        fields = ('name', 'level', 'keywords')


class LanguageSerializer(WritableNestedModelSerializer):

    class Meta:
        model = Language
        fields = ('language', 'fluency')


class InterestSerializer(WritableNestedModelSerializer):
    keywords = KeywordSerializer(many=True)

    class Meta:
        model = Interest
        fields = ('name', 'keywords')


class ReferenceSerializer(WritableNestedModelSerializer):

    class Meta:
        model = Reference
        fields = ('name', 'reference')


class ResumeSerializer(WritableNestedModelSerializer):
    basics = BasicSerializer()
    work = WorkSerializer(many=True)
    volunteer = VolunteerSerializer(many=True)
    education = EducationSerializer(many=True)
    awards = AwardSerializer(many=True)
    publications = PublicationSerializer(many=True)
    skills = SkillSerializer(many=True)
    languages = LanguageSerializer(many=True)
    interests = InterestSerializer(many=True)
    references = ReferenceSerializer(many=True)

    class Meta:
        model = Resume
        fields = ('basics', 'work', 'volunteer', 'education', 'awards', 
                  'publications', 'skills', 'languages', 'interests', 'references')