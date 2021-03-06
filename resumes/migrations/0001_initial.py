# Generated by Django 3.2 on 2021-04-26 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Basic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('label', models.CharField(max_length=20, null=True)),
                ('picture', models.ImageField(null=True, upload_to='')),
                ('email', models.EmailField(max_length=254, null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('website', models.CharField(max_length=255)),
                ('summary', models.CharField(max_length=255)),
                ('version', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Highlight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, null=True)),
                ('postal_code', models.CharField(max_length=20, null=True)),
                ('city', models.CharField(max_length=150, null=True)),
                ('country_code', models.CharField(max_length=20, null=True)),
                ('region', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basics', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='resumes.basic')),
            ],
        ),
        migrations.CreateModel(
            name='WorkVolunteer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=60, null=True)),
                ('website', models.CharField(max_length=255, null=True)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('summary', models.CharField(max_length=255, null=True)),
                ('highlights', models.ManyToManyField(blank=True, to='resumes.Highlight')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('level', models.CharField(max_length=50)),
                ('keywords', models.ManyToManyField(blank=True, to='resumes.Keyword')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumes.resume')),
            ],
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('reference', models.CharField(max_length=255)),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumes.resume')),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('publisher', models.CharField(max_length=80)),
                ('release_date', models.DateField(null=True)),
                ('website', models.CharField(max_length=255, null=True)),
                ('summary', models.CharField(max_length=255, null=True)),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumes.resume')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network', models.CharField(max_length=60, null=True)),
                ('username', models.CharField(max_length=50, null=True)),
                ('url', models.CharField(max_length=255, null=True)),
                ('basic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumes.basic')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=80)),
                ('fluency', models.CharField(max_length=50)),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumes.resume')),
            ],
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('keywords', models.ManyToManyField(blank=True, to='resumes.Keyword')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumes.resume')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=80)),
                ('area', models.CharField(max_length=50, null=True)),
                ('study_type', models.CharField(max_length=80, null=True)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('gpa', models.CharField(max_length=5, null=True)),
                ('courses', models.ManyToManyField(blank=True, to='resumes.Course')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumes.resume')),
            ],
        ),
        migrations.AddField(
            model_name='basic',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resumes.location'),
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('date', models.DateField(null=True)),
                ('awarder', models.CharField(max_length=80)),
                ('summary', models.CharField(max_length=255, null=True)),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumes.resume')),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('workvolunteer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resumes.workvolunteer')),
                ('company', models.CharField(max_length=80)),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumes.resume')),
            ],
            bases=('resumes.workvolunteer',),
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('workvolunteer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='resumes.workvolunteer')),
                ('organization', models.CharField(max_length=80)),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumes.resume')),
            ],
            bases=('resumes.workvolunteer',),
        ),
    ]
