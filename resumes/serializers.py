from resumes.models import (
    Award, Basic, Course, Education, Highlight, Interest, Keyword, Language,
    Location, Profile, Publication, Resume, Skill, Volunteer, Work
)
from rest_framework import serializers


class LocationSerializer(serializers.ModelSerializer):
    postalCode = serializers.CharField(source='postal_code')
    countryCode = serializers.CharField(source='country_code')

    class Meta:
        model = Location
        fields = ('address', 'postalCode', 'city', 'countryCode', 'region')


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('network', 'username', 'url')


class BasicSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    profiles = ProfileSerializer(many=True)

    class Meta:
        model = Basic
        fields = ('name', 'label', 'picture', 'email', 'phone', 'website',
                  'summary', 'location', 'profiles')


class HighlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Highlight
        fields = ('name',)


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('name',)


class KeywordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Keyword
        fields = ('name',)


class WorkSerializer(serializers.ModelSerializer):
    highlights = HighlightSerializer(many=True)
    startDate = serializers.DateField(source='start_date')
    endDate = serializers.DateField(source='end_date')

    class Meta:
        model = Work
        fields = ('company', 'position', 'website', 'startDate', 'endDate',
                  'summary', 'highlights')


class VolunteerSerializer(serializers.ModelSerializer):
    highlights = HighlightSerializer(many=True)
    startDate = serializers.DateField(source='start_date')
    endDate = serializers.DateField(source='end_date')

    class Meta:
        model = Volunteer
        fields = ('organization', 'position', 'website', 'startDate', 'endDate',
                  'summary', 'highlights')


class EducationSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True)
    studyType = serializers.CharField(source='study_type')
    startDate = serializers.DateField(source='start_date')
    endDate = serializers.DateField(source='end_date')

    class Meta:
        model = Education
        fields = ('institution', 'area', 'studyType', 'startDate', 'endDate',
                  'gpa', 'courses')


class AwardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Award
        fields = ('title', 'date', 'awarder', 'summary')


class PublicationSerializer(serializers.ModelSerializer):
    releaseDate = serializers.DateField(source='release_date')

    class Meta:
        model = Publication
        fields = ('name', 'publisher', 'releaseDate', 'website', 'summary')


class SkillSerializer(serializers.ModelSerializer):
    keywords = KeywordSerializer(many=True)

    class Meta:
        model = Skill
        fields = ('name', 'level', 'keywords')


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ('language', 'fluency')


class InterestSerializer(serializers.ModelSerializer):
    keywords = KeywordSerializer(many=True)

    class Meta:
        model = Interest
        fields = ('name', 'keywords')


class ReferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interest
        fields = ('name', 'reference')


class ResumeSerializer(serializers.modelSerializer):
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