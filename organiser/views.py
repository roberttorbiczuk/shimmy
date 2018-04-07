from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from organiser.forms import ProfileForm


def index(request):
    return render(request, 'organiser/index.html', {})


class AddProfileView(View):

    def get(self, request):
        form = ProfileForm()
        return render(request, 'organiser/profile_form.html', {'form': form})

