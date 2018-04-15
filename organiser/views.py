from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView

from organiser.forms import ProfileForm, UploadFileForm, TemporaryFileForm
from .models import Profile, CSV
from django.contrib.auth.models import Group
import xlrd
from django.utils.dateparse import parse_date

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
            workbook = xlrd.open_workbook(file_contents=request.FILES['file'].read())
            worksheet = workbook.sheet_by_index(2)
            cell = worksheet.cell_value
            for row in range(1, worksheet.nrows):
                if worksheet.cell_type(row, 1) == xlrd.XL_CELL_EMPTY:
                    continue
                try:
                    profile = Profile()
                    name = cell(row, 1).split()
                    profile.first_name = name[0]
                    profile.last_name = name[1]

                    phone_number = str(cell(row, 4)).replace(" ", "")
                    if phone_number:
                        profile.phone = int(float(phone_number))
                    profile.mail = cell(row, 5)
                    status = cell(row, 8).split()
                    if status:
                        profile.status_date = parse_date(status[0].replace('.', '-'))

                    exist_profile = Profile.objects.filter(first_name=name[0], last_name=[1])
                    if not exist_profile:
                        try:
                            profile.save()
                        except Exception as e:
                            print(profile.last_name + ' ' + e)
                except Exception as e:
                    print(e)
            return redirect('list')
        return render(request, 'organiser/base_form.html', {'form': form, 'enctype': 'enctype'})

    def get(self, request):
        form = TemporaryFileForm()
        return render(request, 'organiser/base_form.html', {'form': form, 'enctype': 'enctype'})