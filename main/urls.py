from django.conf.urls import url

from main import views


urlpatterns = [
    url(r'^students$', views.students, name='students'),
    url(r'^all-students$', views.StudentListView.as_view(), name='student_list'),
]
