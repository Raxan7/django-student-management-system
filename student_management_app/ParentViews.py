from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from itertools import chain
import datetime # To Parse input DateTime into Python Date Time Object

from student_management_app.forms import AddParentForm, EditParentForm
from student_management_app.models import CustomUser, Staffs, Parents, Subjects, Students, Attendance, AttendanceReport, LeaveReportStudent, FeedBackStudent, StudentResult, StudentPerformance
from student_management_app.ml_model import load_model


def parent_home(request):
    parent = Parents.objects.get(admin=request.user).child.admin
    student = Students.objects.get(admin=parent)
    student_result = StudentResult.objects.filter(student_id=student.id)

    total = student_result[0].test1_marks + student_result[0].test2_marks + student_result[0].UE_marks
    print(total)


    context = {
        "student_result": student_result,
        "total": total,
    }
    return render(request, "parent_template/parent_view_result.html", context)

        

def parent_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Parents.objects.get(admin=user)

    context={
        "user": user,
        "student": student
    }
    return render(request, 'parent_template/parent_profile.html', context)


def parent_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('parent_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            student = Parents.objects.get(admin=customuser.id)
            student.address = address
            student.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('parent_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('parent_profile')


# AI
def parent_view_predictions(request):


    parent = Parents.objects.get(admin=request.user).child.admin
    student = Students.objects.get(admin=parent)
    student_result = StudentResult.objects.filter(student_id=student.id)

    student_data = StudentPerformance.objects.get(student=student)
    print(student_result)
    test1, test2 = student_result.first().test1_marks, student_result.first().test2_marks
    dataset = [
            student_data.age, student_data.medu, student_data.fedu, student_data.traveltime, student_data.studytime,
              student_data.failures, student_data.famrel, student_data.freetime, student_data.goout, 
              student_data.dalc, student_data.walc, student_data.health, student_data.absences, 
              test1, test2
        ]
    results = load_model().predict([dataset])
    results = round(results[0] / 20 * 60, 2)

    total = test1 + test2 + results

    # Add messages to indicate the prediction result
    if total >= 40:
        messages.success(request, f"Congratulations! Your predicted total score is {total}. You are likely to pass in your exams!")
    else:
        messages.error(request, f"Sorry! Your predicted total score is {total}. You are in danger of failing, work harder!.")

    context = {
        "student_result": student_result,
        "results": results,
        "total": total,
    }
    return render(request, "parent_template/parent_view_predictions.html", context)
