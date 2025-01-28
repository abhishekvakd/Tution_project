from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login1',views.login1,name='login1'),
    path('teacher',views.teacher,name='teacher'),
    path('student',views.student,name='student'),


    path('add_teacher',views.add_teacher,name='add_teacher'),
    path('add_student',views.add_student,name='add_student'),
    path('log_user',views.log_user,name='log_user'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('reset',views.reset,name='reset'),
    path('reset_pass',views.reset_pass,name='reset_pass'),





    path('adminhome',views.adminhome,name='adminhome'),
    path('approvedisapprove',views.approvedisapprove,name='approvedisapprove'),
    path('approve<int:k>',views.approve,name='approve'),
    path('disapprove<int:k>',views.disapprove,name='disapprove'),


    path('teacher_home',views.teacher_home,name='teacher_home'),
    path('student_home',views.student_home,name='student_home'),




]
