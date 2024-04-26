from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture

from student_management_app.models import CustomUser, PredictionModel, Parents, Students, StudentResult


def parent_home(request):
    parent = Parents.objects.get(admin=request.user).child.admin
    student = Students.objects.get(admin=parent)
    student_result = StudentResult.objects.filter(student_id=student.id)

    context = {
        "student_result": student_result,
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

    obj = PredictionModel.objects.filter(exam__student_id__id=student.id)
    for i in obj:
        # Add messages to indicate the prediction result
        if i.total_CA >= 40:
            messages.success(request, f"Congratulations! Your child's predicted total score is {round(i.total_CA, 1)}. Your child has a high ptobability of passing the exams!")
        else:
            messages.error(request, f"Sorry! Your child's predicted total score is {round(i.total_CA, 1)}. Your child is in danger of failing!.")

    context = {
        "student_result": obj
    }
    return render(request, "parent_template/parent_view_predictions.html", context)
