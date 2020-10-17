# Generated by Django 3.1.2 on 2020-10-12 19:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContributorDeliverable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('function', models.CharField(choices=[('AUTHOR', 'Author'), ('VALIDATOR', 'Validator'), ('COLLABORATOR', 'Collaborator')], default='Author', max_length=20)),
                ('feedback', models.CharField(choices=[('NOTKNOWN', 'Not Known'), ('AGREED', 'Agreed'), ('DISAGREED', 'Disagreed')], default='Not Known', max_length=20)),
                ('comment', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='ContributorProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addingDate', models.DateField(default=django.utils.timezone.now)),
                ('removingDate', models.DateField(default=django.utils.timezone.now)),
                ('permission', models.CharField(choices=[('PM', 'Project Manager'), ('CONTRIB', 'Contributor')], default='Project Manager', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('creationDate', models.DateField(default=django.utils.timezone.now)),
                ('dueDate', models.DateField(default=django.utils.timezone.now)),
                ('deletionDate', models.DateField(default=django.utils.timezone.now)),
                ('closureDate', models.DateField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('NEW', 'Just created'), ('ON GOING', 'On going'), ('FINISHED', 'Finished'), ('DELETED', 'Deleted')], default='NEW', max_length=20)),
                ('advancement', models.FloatField(default=1)),
                ('description', models.CharField(default='No description yet', max_length=150)),
                ('contributor', models.ManyToManyField(through='project.ContributorProject', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Deliverable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=251)),
                ('addingDate', models.DateField(default=django.utils.timezone.now)),
                ('dueDate', models.DateField(default=django.utils.timezone.now)),
                ('closureDate', models.DateField(default=django.utils.timezone.now)),
                ('deletionDate', models.DateField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('NEW', 'Just created'), ('APPROVAL ON GOING', 'Approval on going'), ('APPROVED', 'Approved'), ('DELETED', 'Deleted')], default='NEW', max_length=20)),
                ('progression', models.FloatField(default=1, max_length=505)),
                ('contributor', models.ManyToManyField(through='project.ContributorDeliverable', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project')),
            ],
        ),
        migrations.AddField(
            model_name='contributorproject',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project'),
        ),
        migrations.AddField(
            model_name='contributorproject',
            name='projectPlannerUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contributordeliverable',
            name='deliverable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributor_deliverable', to='project.deliverable'),
        ),
        migrations.AddField(
            model_name='contributordeliverable',
            name='projectPlannerUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributor_deliverable', to=settings.AUTH_USER_MODEL),
        ),
    ]