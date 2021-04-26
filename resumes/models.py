from django.db import models
from model_utils import FieldTracker

class Location(models.Model):
    address = models.CharField(max_length=255, null=True)
    postal_code = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=150, null=True)
    country_code = models.CharField(max_length=20, null=True)
    region = models.CharField(max_length=50, null=True)


class Basic(models.Model):
    name = models.CharField(max_length=80)
    label = models.CharField(max_length=20, null=True)
    picture = models.ImageField(null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=15, null=True)
    website = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    version = models.IntegerField(default=0)

    tracker = FieldTracker()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.version += 1
        return super().save(*args, **kwargs)


class Profile(models.Model):
    basic = models.ForeignKey(Basic, on_delete=models.CASCADE, related_name='profiles')
    network = models.CharField(max_length=60, null=True)
    username = models.CharField(max_length=50, null=True)
    url = models.CharField(max_length=255, null=True)
    version = models.IntegerField(default=0)

    tracker = FieldTracker()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.version += 1
        return super().save(*args, **kwargs)


class Resume(models.Model):
    basics = models.OneToOneField(Basic, on_delete=models.CASCADE)
    version = models.IntegerField(default=0)

    tracker = FieldTracker()

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.version += 1
        return super().save(*args, **kwargs)

class Highlight(models.Model):
    name = models.CharField(max_length=255)


class Course(models.Model):
    name = models.CharField(max_length=255)


class Keyword(models.Model):
    name = models.CharField(max_length=255)


class WorkVolunteer(models.Model):
    position = models.CharField(max_length=60, null=True)
    website = models.CharField(max_length=255, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    summary = models.CharField(max_length=255, null=True)
    highlights = models.ManyToManyField(Highlight, blank=True)

    tracker = FieldTracker()


class Work(WorkVolunteer):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='work')
    company = models.CharField(max_length=80)

    tracker = FieldTracker()


class Volunteer(WorkVolunteer):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='volunteer')
    organization = models.CharField(max_length=80)

    tracker = FieldTracker()


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=80)
    area = models.CharField(max_length=50, null=True)
    study_type = models.CharField(max_length=80, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    gpa = models.CharField(max_length=5, null=True)
    courses = models.ManyToManyField(Course, blank=True)

    tracker = FieldTracker()


class Award(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='awards')
    title = models.CharField(max_length=80)
    date = models.DateField(null=True)
    awarder = models.CharField(max_length=80)
    summary = models.CharField(max_length=255, null=True)

    tracker = FieldTracker()


class Publication(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='publications')
    name = models.CharField(max_length=80)
    publisher = models.CharField(max_length=80)
    release_date = models.DateField(null=True)
    website = models.CharField(max_length=255, null=True)
    summary = models.CharField(max_length=255, null=True)
    
    tracker = FieldTracker()


class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=80)
    level = models.CharField(max_length=50)
    keywords = models.ManyToManyField(Keyword, blank=True)

    tracker = FieldTracker()


class Language(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='languages')
    language = models.CharField(max_length=80)
    fluency = models.CharField(max_length=50)

    tracker = FieldTracker()


class Interest(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='interests')
    name = models.CharField(max_length=80)
    keywords = models.ManyToManyField(Keyword, blank=True)

    tracker = FieldTracker()


class Reference(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='references')
    name = models.CharField(max_length=80)
    reference = models.CharField(max_length=255)

    tracker = FieldTracker()
