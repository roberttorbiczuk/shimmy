from django.contrib.auth.models import User, Group
from django.db import models
from django.utils import timezone


DANCE_ROLE = (
    ('F', 'Follow'),
    ('L', 'Lead'),
)


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, default=None, null=True, blank=True, on_delete=models.SET_NULL)
    phone = models.IntegerField(null=True, blank=True)
    dance_role = models.CharField(choices=DANCE_ROLE, max_length=10)
    rodo_delaration = models.FileField(upload_to='rodo_directory_path')
    status = models.CharField(max_length=100, default=None)
    status_date = models.CharField(max_length=100, default=None)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.id:
            self.user.is_active = False
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Person, self).save(*args, **kwargs)

    @property
    def rodo_directory_path(self, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'usersfiles/user_{0}/rodo_{1}'.format(self.user.id, filename)

    def get_current_time(self):
        return timezone.now()