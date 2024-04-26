from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver



class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()



# Overriding the Default Django Auth User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Staff"), (3, "Student"), (4, "Parent"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)



class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    # def __str__(self):
	#     return self.course_name



class Subjects(models.Model):
    id =models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1) #need to give defauult course
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    address = models.TextField()
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, default=1)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Parents(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.TextField()
    child = models.OneToOneField(Students, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Attendance(models.Model):
    # Subject Attendance
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class AttendanceReport(models.Model):
    # Individual Student Attendance
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    stafff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    test1_marks = models.FloatField(default=0, blank=True, null=True)
    test2_marks = models.FloatField(default=0, blank=True, null=True)
    UE_marks = models.FloatField(default=0, blank=True, null=True)
    total_CA = models.FloatField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class PredictionModel(models.Model):
    id = models.AutoField(primary_key=True)
    exam = models.ForeignKey(StudentResult, on_delete=models.CASCADE, related_name="exam", null=False)
    # student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    # subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    test1_marks = models.FloatField(default=0, blank=True, null=True)
    test2_marks = models.FloatField(default=0, blank=True, null=True)
    UE_prediction = models.FloatField(default=0, blank=True, null=True)
    total_CA = models.FloatField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self) -> str:
        return f"Predictions for {self.exam}"


class StudentPerformance(models.Model):
    SEX_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    ADDRESS_CHOICES = (
        ('U', 'Urban'),
        ('R', 'Rural'),
    )
    FAMSIZE_CHOICES = (
        ('LE3', 'Less or equal to 3'),
        ('GT3', 'Greater than 3'),
    )
    PSTATUS_CHOICES = (
        ('T', 'Living together'),
        ('A', 'Apart'),
    )
    EDU_CHOICES = (
        (0, 'None'),
        (1, 'Primary education (4th grade)'),
        (2, '5th to 9th grade'),
        (3, 'Secondary education'),
        (4, 'Higher education'),
    )
    JOB_CHOICES = (
        ('teacher', 'Teacher'),
        ('health', 'Health care related'),
        ('services', 'Civil services'),
        ('at_home', 'At home'),
        ('other', 'Other'),
    )
    REASON_CHOICES = (
        ('home', 'Close to home'),
        ('reputation', 'School reputation'),
        ('course', 'Course preference'),
        ('other', 'Other'),
    )
    GUARDIAN_CHOICES = (
        ('mother', 'Mother'),
        ('father', 'Father'),
        ('other', 'Other'),
    )
    YES_NO_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )
    TRAVEL_TIME_CHOICES = [(i, f'{i} hours') for i in range(1, 5)]
    STUDY_TIME_CHOICES = [(i, f'{i} hours') for i in range(1, 11)]
    FAILURE_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4 or more'),
    )
    GRADE_CHOICES = [(i, str(i)) for i in range(0, 21)]
    HEALTH_CHOICES = (
        (1, 'Very bad'),
        (2, 'Bad'),
        (3, 'Normal'),
        (4, 'Good'),
        (5, 'Very good'),
    )

    objects = models.Manager()
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='student')
    age = models.IntegerField(default=18, blank=True, null=True)
    address = models.CharField(max_length=1, choices=ADDRESS_CHOICES, default='Unspecified', blank=True, null=True)
    medu = models.IntegerField(choices=EDU_CHOICES, default=0, blank=True, null=True)
    fedu = models.IntegerField(choices=EDU_CHOICES, default=0, blank=True, null=True)
    traveltime = models.IntegerField(choices=TRAVEL_TIME_CHOICES, default=0, blank=True, null=True)
    studytime = models.IntegerField(choices=STUDY_TIME_CHOICES, default=0, blank=True, null=True)
    failures = models.IntegerField(choices=FAILURE_CHOICES, default=0, blank=True, null=True)
    famrel = models.IntegerField(default=0, blank=True, null=True)
    freetime = models.IntegerField(default=0, blank=True, null=True)
    goout = models.IntegerField(default=0, blank=True, null=True)
    dalc = models.IntegerField(default=0, blank=True, null=True)
    walc = models.IntegerField(default=0, blank=True, null=True)
    health = models.IntegerField(choices=HEALTH_CHOICES, default=0, blank=True, null=True)
    absences = models.IntegerField(default=0, blank=True, null=True)
    g1 = models.IntegerField(choices=GRADE_CHOICES, verbose_name='First period grade', default=0)
    g2 = models.IntegerField(choices=GRADE_CHOICES, verbose_name='Second period grade', default=0)

    def __str__(self):
        return f"Data for a {self.age}"



#Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance)
        if instance.user_type == 3:
            Students.objects.create(admin=instance, course_id=Courses.objects.get(id=1), session_year_id=SessionYearModel.objects.get(id=1), address="", profile_pic="", gender="")
        if instance.user_type == 4:
            Parents.objects.create(admin=instance, child_id=Students.objects.get(id=1).id, address="")
    

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.students.save()
    if instance.user_type == 4:
        instance.parents.save() 