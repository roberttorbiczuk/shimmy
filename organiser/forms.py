from django import forms
from organiser.models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ['created', 'modified', 'rodo_declaration']

    # To add widget in simple way
    # def __init__(self, *args, **kwargs):
    #     super(ProfileForm, self).__init__(*args, **kwargs)
    #     for key, field in self.fields.items():
    #         print(key, field)
    #         if key == 'status_date':
    #             field.widget.attrs['type'] = 'date'
