from django.urls import path

from .views import index, AddProfileView, ListProfileView, EditProfileView, DeleteProfileView, GroupView, \
    GroupsListView, UploadFileView, ImportDataFromFileView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index, name='index'),
    path('add_user/', AddProfileView.as_view(), name='add'),
    path('list/', ListProfileView.as_view(), name='list'),
    path('edit/<int:pk>/', EditProfileView.as_view(), name='edit'),
    path('delete/<int:pk>/', DeleteProfileView.as_view(), name='delete'),
    path('group/<int:pk>/', GroupView.as_view(), name='group'),
    path('group/list/', GroupsListView.as_view(), name='groups_list'),
    path('upload/', UploadFileView.as_view(), name='upload'),
    path('import/', ImportDataFromFileView.as_view(), name='import'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
