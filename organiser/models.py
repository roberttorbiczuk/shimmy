from django.contrib.auth.models import User, Group
from django.db import models
from django.utils import timezone


DANCE_ROLE = (
    ('F', 'Follower'),
    ('L', 'Leader'),
)


class Profile(models.Model):
    first_name = models.CharField('Imię', max_length=20)
    last_name = models.CharField('Nazwisko', max_length=30)
    mail = models.EmailField(null=True, blank=True)
    partner = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Partner')
    group = models.ManyToManyField(Group, default=None, blank=True, verbose_name='Grupa')
    phone = models.IntegerField('Telefon', null=True, blank=True)
    dance_role = models.CharField('Lead or Follow', choices=DANCE_ROLE, max_length=10, default='Follow')
    rodo_declaration = models.FileField('Deklaracja rodo', upload_to='rodo_directory_path', default=None, null=True, blank=True)
    status = models.CharField('Status', max_length=100, default=None, null=True, blank=True)
    status_date = models.DateField('Data wysłania', max_length=20, default=None, null=True, blank=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Profile, self).save(*args, **kwargs)

    def get_current_time(self):
        return timezone.now()

    def get_quantity(self):
        return self.group.count()

    @property
    def get_rodo_directory_path(self, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/rodo_<filename>
        return 'usersfiles/user_{0}/rodo_{1}'.format(self.user.id, filename)
