# from channels.auth import login, logout
import os
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from student_management_app.EmailBackEnd import EmailBackEnd
from student_management_app.csv_imports import test1_extraction, BASE_DIR


def home(request):
    print("home view here")
    return render(request, 'index.html')


def loginPage(request):
    print("login view here")
    csv_file_path = os.path.join(BASE_DIR, "student_management_app/trial.csv")
    test1_extraction(csv_file_path)
    return render(request, 'login.html')



def doLogin(request):
    print("doLogin view here")
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        print("Hi")
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            print(user_type)
            #return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            if user_type == '1':
                return redirect('admin_home')
                
            elif user_type == '2':
                # return HttpResponse("Staff Login")
                return redirect('staff_home')
                
            elif user_type == '3':
                # return HttpResponse("Student Login")
                return redirect('student_home')
            
            elif user_type == '4':
                # return HttpResponse("Parent Login")
                return redirect('parent_home')
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            # return HttpResponseRedirect("/")
            return redirect('login')



def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")



def logout_user(request):
    logout(request)
    print("logout view here")
    return HttpResponseRedirect('/')


