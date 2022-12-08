from django.urls import path
from django.conf.urls import include

from . import views

app_name= "main"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), 
    path('workers', views.WorkersView.as_view(), name='workers'), 
    path('books', views.BooksView.as_view(), name='books'), 
    path('groups', views.GroupsView.as_view(), name='groups'), 
    path('roles', views.RolesView.as_view(), name='roles'), 
    path('logs', views.LogsView.as_view(), name='logs'), 

    path('delete', views.DeleteView.as_view(), name='delete'), 

    path('student/edit', views.StudentEditView.as_view(), name='student_edit'), 
    path('worker/edit', views.WorkerEditView.as_view(), name='worker_edit'), 
    path('book/edit', views.BookEditView.as_view(), name='book_edit'), 
    path('group/edit', views.GroupEditView.as_view(), name='group_edit'), 
    path('role/edit', views.RoleEditView.as_view(), name='role_edit'), 
    path('log/edit', views.LogEditView.as_view(), name='log_edit'), 

    path('login', views.LoginView.as_view(), name='login'), 
    path('logout', views.LogoutView.as_view(), name='logout'), 
    path('register', views.RegisterView.as_view(), name='register'),
]