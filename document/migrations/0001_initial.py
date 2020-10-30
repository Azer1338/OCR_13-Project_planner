import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('loadingDate', models.DateField(default=django.utils.timezone.now)),
                ('link', cloudinary.models.CloudinaryField(max_length=255, verbose_name='link')),
                ('deliverable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.deliverable')),
            ],
        ),
    ]
