from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView

from organiser.forms import ProfileForm, UploadFileForm, TemporaryFileForm
from .models import Profile, CSV
from django.contrib.auth.models import Group
import xlrd
import os
from django.conf import settings


def index(request):
    return render(request, 'organiser/index.html', {})


class AddProfileView(View):

    def get(self, request):
        form = ProfileForm()
        return render(request, 'organiser/base_form.html', {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST)
        print('Tutaj')
        if form.is_valid():
            form.save()
            return redirect('list')
        return render(request, 'organiser/base_form.html', {'form': form})


class ListProfileView(ListView):

    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EditProfileView(View):

    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        form = ProfileForm(instance=profile)
        return render(request, 'organiser/base_form.html', {'form': form})

    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('list')
        return render(request, 'organiser/base_form.html', {'form': form})


class DeleteProfileView(DeleteView):
    model = Profile
    success_url = reverse_lazy('list')


class GroupView(View):

    def get(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        profiles = group.profile_set.all()
        return render(request, 'organiser/group.html', {'group': group,
                                                        'profiles': profiles})


class GroupsListView(ListView):

    model = Group
    template_name = 'organiser/group_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UploadFileView(View):

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list')
        return render(request, 'organiser/base_form.html', {'form': form, 'enctype': 'enctype'})

    def get(self, request):
        form = UploadFileForm()
        return render(request, 'organiser/base_form.html', {'form': form, 'enctype': 'enctype'})


class ImportDataFromFileView(View):

    def post(self, request):
        form = TemporaryFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            path_to_file = settings.MEDIA_ROOT + '/temporary/' + request.FILES.get('file').name
            workbook = xlrd.open_workbook(os.path.abspath(path_to_file))
            worksheet = workbook.sheet_by_index(3)
            cell = worksheet.cell_value
            for row in range(worksheet.nrows):
                try:
                    profile = Profile()
                    name = cell(row+1, 1).split()
                    profile.first_name = name[0]
                    profile.last_name = name[1]
                    profile.phone = int(cell(row+1, 4))
                    status = cell(row+1, 8).split()
                    if status:
                        profile.status = status[0]
                    try:
                        profile.save()
                    except:
                        print("coś poszło nie tak")
                except:
                    print("coś poszło nie tak")
            os.remove(path_to_file)
            return redirect('list')
        return render(request, 'organiser/base_form.html', {'form': form, 'enctype': 'enctype'})

    def get(self, request):
        form = TemporaryFileForm()
        return render(request, 'organiser/base_form.html', {'form': form, 'enctype': 'enctype'})