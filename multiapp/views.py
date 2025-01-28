from django.shortcuts import render,redirect
from .models import CustomUser
from .models import Teacher
from .models import Student
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import auth
from django.db.models import Q
import random

# Create your views here.
def home(request):
    return render(request, 'home.html')

def login1(request):
    return render(request, 'login.html')

def teacher(request):
    return render(request, 'teacher.html')

def student(request):
    return render(request, 'student.html')

def add_teacher(request):
    if request.method=='POST':
        firstname=request.POST['first_name']
        lastname=request.POST['last_name']
        username=request.POST['username']
        age=request.POST['age']
        email=request.POST['email']
        contact=request.POST['contact']
        user_type=request.POST['text']
        course=request.POST['course']
        image=request.FILES.get('file')

        if CustomUser.objects.filter(username=username).exists():
            messages.success(request, 'Username already exists. Please choose another. ')
            return redirect('teacher')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.success(request, 'Email already exists. Please choose another. ')
            return redirect('teacher')
        
        user = CustomUser.objects.create_user(
            username=username,
            first_name=firstname,
            last_name=lastname,
            email=email,
            user_type=user_type

        ) 
        user.save()

        teacher=Teacher(
            user=user,
            course=course,
            age=age,
            phone_number=contact,
            image=image
        )
        teacher.save()
        messages.success(request, 'Registration Successful !Please wait for admin approval')
        return redirect('teacher')
    


def add_student(request):
    if request.method=='POST':
        firstname=request.POST['first_name']
        lastname=request.POST['last_name']
        username=request.POST['username']
        age=request.POST['age']
        email=request.POST['email']
        contact=request.POST['contact']
        user_type=request.POST['text']
        course=request.POST['course']
        image=request.FILES.get('file')

        if CustomUser.objects.filter(username=username).exists():
            messages.success(request, 'Username already exists. Please choose another. ')
            return redirect('student')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.success(request, 'Email already exists. Please choose another. ')
            return redirect('student')
        
        user = CustomUser.objects.create_user(
            username=username,
            first_name=firstname,
            last_name=lastname,
            email=email,
            user_type=user_type

        ) 
        user.save()

        student=Student(
            user=user,
            course=course,
            age=age,
            phone_number=contact,
            image=image
        )
        student.save()
        messages.success(request, 'Registration Successful !Please wait for admin approval')
        return redirect('student')
    

def log_user(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)

        if user is not None:
            if user.user_type=='1':
                login(request,user)
                return redirect('adminhome')
            elif user.user_type=='2':
                login(request,user)
                return redirect('teacher_home')
            elif user.user_type=='3':
                login(request,user)
                return redirect('student_home')
            
        else:
            messages.info(request, 'invalid username or password')
            return redirect('login1')


def adminhome(request):
    unapproved_count=CustomUser.objects.filter(status=0).count()
    count=unapproved_count-1
    print(count)
    return render(request, 'adminhome.html' , {'unapproved_count':count})

def approvedisapprove(request):
    users=CustomUser.objects.filter(~Q(user_type="1"))
    unapproved_count=CustomUser.objects.filter(status=0).count()
    count=unapproved_count-1
    print(count)
    return render(request, 'approvedisapprove.html', {'user_data':users , 'unapproved_count':count})

def approve(request,k):
    usr = CustomUser.objects.get(id=k)
    usr.status=1
    usr.save()

    if usr.user_type == '2':
        tea = Teacher.objects.get(user=k)
        password= str(random.randint(100000, 999999))
        print(password)
        usr.set_password(password)
        usr.save()

        send_mail(
            'Admin approved',
            f"Username: {tea.user.username}\nPassword: {password}\nEmail: {tea.user.email}",
            settings.EMAIL_HOST_USER,
            [tea.user.email]

        )
        messages.info(request, 'Teacher approved')

    elif usr.user_type == '3':
        stu = Student.objects.get(user=k)
        password= str(random.randint(100000, 999999))
        print(password)
        usr.set_password(password)
        usr.save()

        send_mail(
            'Admin approved',
            f"Username: {stu.user.username}\nPassword: {password}\nEmail: {stu.user.email}",
            settings.EMAIL_HOST_USER,
            [stu.user.email]

        )
        messages.info(request, 'Student approved')

    return redirect('approvedisapprove')

def disapprove(request,k):
    usr= CustomUser.objects.get(id=k)
    if usr.user_type=='2':
        Teacher.objects.filter(user=k).delete()
    elif usr.user_type=='3':
        Student.objects.filter(user=k).delete()
    usr.delete()
    send_mail(
    'Admin disapproved',
    f"Dear {usr.username},\n\nSorry, admin has disapproved your request.\n\nBest regards,\nAdmin",
    settings.EMAIL_HOST_USER,
    [usr.email]
    )

    messages.info(request, 'User disapproved')
    return redirect('approvedisapprove')


def student_home(request):
    return render(request, 'thome.html')

def teacher_home(request):
    return render(request, 'shome.html')

def user_logout(request):
    auth.logout(request)
    return redirect('home')

def reset(request):
    return render(request, 'reset.html')

def reset_pass(request):
    if request.method=='POST':
        pas=request.POST['new_password']
        cpas=request.POST['Confirm_password']
        if pas==cpas:
            if len(pas) < 6 or not any(char.isupper() for char in pas) \
                or not any(char.isdigit() for char in pas) \
                or not any(char in '!@#$%^&*()_=+-[]{}|;:,.<>?/~' for char in pas ):
                messages.error(request, 'password must be at least 6 characters long and contain at least one capital letter and at least one special character ')
                return redirect('reset')
            else:
                usr = request.user.id
                tsr=CustomUser.objects.get(id=usr)
                tsr.password=pas
                tsr.set_password(pas)
                tsr.save()
                messages.info(request, 'password changed')
                return redirect('reset')