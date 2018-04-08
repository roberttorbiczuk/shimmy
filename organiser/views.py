from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView

from organiser.forms import ProfileForm
from .models import Profile
from django.contrib.auth.models import Group


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
        group = get_object_or_404(Group, pk=pk).profile_set.all()
        return render(request, 'organiser/group.html', {'group': group})


class GroupsListView(ListView):

    model = Group
    template_name = 'organiser/group_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
