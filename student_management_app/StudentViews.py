from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from itertools import chain
import datetime # To Parse input DateTime into Python Date Time Object

from student_management_app.forms import AddParentForm, EditParentForm
from student_management_app.models import CustomUser, PredictionModel, Courses, Subjects, Students, Attendance, AttendanceReport, LeaveReportStudent, FeedBackStudent, StudentResult, StudentPerformance
from student_management_app.ml_model import load_model


def student_home(request):
    student_obj = Students.objects.get(admin=request.user.id)
    total_attendance = AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present = AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=student_obj, status=False).count()

    course_obj = Courses.objects.get(id=student_obj.course_id.id)
    total_subjects = Subjects.objects.filter(course_id=course_obj).count()

    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subjects.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True, student_id=student_obj.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False, student_id=student_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)
    
    context={
        "total_attendance": total_attendance,
        "attendance_present": attendance_present,
        "attendance_absent": attendance_absent,
        "total_subjects": total_subjects,
        "subject_name": subject_name,
        "data_present": data_present,
        "data_absent": data_absent
    }
    return render(request, "student_template/student_home_template.html", context)


def student_view_attendance(request):
    student = Students.objects.get(admin=request.user.id) # Getting Logged in Student Data
    course = student.course_id # Getting Course Enrolled of LoggedIn Student
    # course = Courses.objects.get(id=student.course_id.id) # Getting Course Enrolled of LoggedIn Student
    subjects = Subjects.objects.filter(course_id=course) # Getting the Subjects of Course Enrolled
    context = {
        "subjects": subjects
    }
    return render(request, "student_template/student_view_attendance.html", context)


def student_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_view_attendance')
    else:
        # Getting all the Input Data
        subject_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Parsing the date data into Python object
        start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Getting all the Subject Data based on Selected Subject
        subject_obj = Subjects.objects.get(id=subject_id)
        # Getting Logged In User Data
        user_obj = CustomUser.objects.get(id=request.user.id)
        # Getting Student Data Based on Logged in Data
        stud_obj = Students.objects.get(admin=user_obj)

        # Now Accessing Attendance Data based on the Range of Date Selected and Subject Selected
        attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse, end_date_parse), subject_id=subject_obj)
        # Getting Attendance Report based on the attendance details obtained above
        attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=stud_obj)

        # for attendance_report in attendance_reports:
        #     print("Date: "+ str(attendance_report.attendance_id.attendance_date), "Status: "+ str(attendance_report.status))

        # messages.success(request, "Attendacne View Success")

        context = {
            "subject_obj": subject_obj,
            "attendance_reports": attendance_reports
        }

        return render(request, 'student_template/student_attendance_data.html', context)
       

def student_apply_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'student_template/student_apply_leave.html', context)


def student_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        student_obj = Students.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(student_id=student_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('student_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('student_apply_leave')


def student_feedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'student_template/student_feedback.html', context)


def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = Students.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStudent(student_id=student_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('student_feedback')


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)

    context={
        "user": user,
        "student": student
    }
    return render(request, 'student_template/student_profile.html', context)


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
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

            student = Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')


def student_view_result(request):
    student = Students.objects.get(admin=request.user.id)
    student_result = StudentResult.objects.filter(student_id=student.id)    

    context = {
        "student_result": student_result,
    }
    return render(request, "student_template/student_view_result.html", context)


# AI
def student_view_predictions(request):
    student = Students.objects.get(admin=request.user.id)
    # student_result = StudentResult.objects.filter(student_id=student.id)
    # student_data = StudentPerformance.objects.get(student=student)
    obj = PredictionModel.objects.filter(exam__student_id__id=student.id)
    for i in obj:
        # Add messages to indicate the prediction result
        if i.total_CA >= 40:
            messages.success(request, f"Congratulations! Your predicted total score is {round(i.total_CA, 1)}. You are likely to pass in your exams!")
        else:
            messages.error(request, f"Sorry! Your predicted total score is {round(i.total_CA, 1)}. You are in danger of failing, work harder!.")

    context = {
        "student_result": obj,
    }
    return render(request, "student_template/student_view_predictions.html", context)


def student_learn_more(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)

    if request.method == 'POST':
        # If the request method is POST, it means the form is submitted
        # Get the data from the request
        age = request.POST.get('age')
        address = request.POST.get('address_choices')
        medu = request.POST.get('medu')
        fedu = request.POST.get('fedu')
        traveltime = request.POST.get('traveltime')
        studytime = request.POST.get('studytime')
        failures = request.POST.get('failures')
        famrel = request.POST.get('famrel')
        freetime = request.POST.get('freetime')
        goout = request.POST.get('goout')
        dalc = request.POST.get('dalc')
        walc = request.POST.get('walc')
        health = request.POST.get('health')
        absences = request.POST.get('absences')

        try:
            student_performance = StudentPerformance.objects.get(student=student)
            # Update the fields
            student_performance.age = age
            student_performance.address = address
            student_performance.medu = medu
            student_performance.fedu = fedu
            # Update other fields similarly
            student_performance.traveltime = traveltime
            student_performance.studytime = studytime
            student_performance.failures = failures
            student_performance.famrel = famrel
            student_performance.freetime = freetime
            student_performance.goout = goout
            student_performance.dalc = dalc
            student_performance.walc = walc
            student_performance.health = health
            student_performance.absences = absences
            student_performance.save()

        except StudentPerformance.DoesNotExist:
            # If the instance doesn't exist, create a new one
            StudentPerformance.objects.create(
                student=student,
                age=age,
                address=address,
                medu=medu,
                fedu=fedu,
                # Add other fields similarly
                traveltime=traveltime,
                studytime=studytime,
                failures=failures,
                famrel=famrel,
                freetime=freetime,
                goout=goout,
                dalc=dalc,
                walc=walc,
                health=health,
                absences=absences,
            )

        # Redirect to the same page after form submission to avoid duplicate submissions
        return HttpResponseRedirect(reverse('student_learn_more'))

    else:
        # If the request method is GET, render the form
        # Fetching choices for select dropdowns from the model itself
        address_choices = StudentPerformance.ADDRESS_CHOICES
        edu_choices = StudentPerformance.EDU_CHOICES
        traveltime_choices = StudentPerformance.TRAVEL_TIME_CHOICES
        studytime_choices = StudentPerformance.STUDY_TIME_CHOICES
        failure_choices = StudentPerformance.FAILURE_CHOICES
        health_choices = StudentPerformance.HEALTH_CHOICES

        context={
            "user": user,
            "student": student,
            "address_choices": address_choices,
            "edu_choices": edu_choices,
            "traveltime_choices": traveltime_choices,
            "studytime_choices": studytime_choices,
            "failure_choices": failure_choices,
            "health_choices": health_choices,
        }
        return render(request, 'student_template/student_learn_more.html', context)


# Views to add parent
def add_parent(request):
    form = AddParentForm()
    context = {
        "form": form
    }
    return render(request, 'student_template/add_parent_template.html', context)




def add_parent_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_parent')
    else:
        form = AddParentForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            gender = form.cleaned_data['gender']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None


            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=4)
                user.parents.address = address

                user.parents.child = Students.objects.get(admin=request.user)

                user.parents.gender = gender
                user.parents.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "Parent Added Successfully!")
                return redirect('add_parent')
            except Exception as e:
                messages.error(request, "Failed to Add Parent!")
                print(e)
                return redirect('add_parent')
        else:
            return redirect('add_parent')


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
