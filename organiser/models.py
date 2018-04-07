from django.contrib.auth.models import User, Group
from django.db import models
from django.utils import timezone


DANCE_ROLE = (
    ('F', 'Follow'),
    ('L', 'Lead'),
)


class Profile(models.Model):
    first_name = models.CharField('Imię', max_length=20)
    last_name = models.CharField('Nazwisko', max_length=30)
    group = models.ForeignKey(Group, default=None, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Grupa')
    phone = models.IntegerField('Telefon', null=True, blank=True)
    dance_role = models.CharField('Lead or Follow', choices=DANCE_ROLE, max_length=10, default='Follow')
    rodo_declaration = models.FileField('Deklaracja rodo', upload_to='rodo_directory_path', default=None, null=True, blank=True)
    status = models.CharField('Status', max_length=100, default=None)
    status_date = models.DateField('Data wysłania', max_length=20, default=None)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.id:
            self.user.is_active = False
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Profile, self).save(*args, **kwargs)

    @property
    def rodo_directory_path(self, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'usersfiles/user_{0}/rodo_{1}'.format(self.user.id, filename)

    def get_current_time(self):
        return timezone.now()