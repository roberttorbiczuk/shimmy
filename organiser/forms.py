from django import forms
from organiser.models import Profile, CSV, TemporaryXLSFile
from django.contrib.auth.models import Group


class ProfileForm(forms.ModelForm):

    group = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Group.objects.all(), label='Grupa')

    class Meta:
        model = Profile
        exclude = ['created', 'modified', 'rodo_declaration']


    # To add widget in simple way
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if isinstance(field.widget, forms.DateInput):
                field.widget.attrs['title'] = 'Podaj datę w formacie DD.MM.YYYY'
                field.widget.attrs.update({'placeholder': 'DD.MM.YYYY'})


class UploadFileForm(forms.ModelForm):

    class Meta:
        model = CSV
        fields = '__all__'


class TemporaryFileForm(forms.ModelForm):

    class Meta:
        model = TemporaryXLSFile
        fields = '__all__'
