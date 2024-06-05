import csv
import os
from student_management_app.models import Dummy
from pathlib import Path
from django.db import transaction

BASE_DIR = Path(__file__).resolve().parent.parent



def test1_extraction(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        csv_data = list(reader)
        
        # Extract the names from the CSV data
        csv_names = [row['name'] for row in csv_data]
        
        # Fetch existing records in one query
        existing_records = Dummy.objects.filter(name__in=csv_names).values_list('name', flat=True)
        existing_names = set(existing_records)
        
        # Prepare the new records to be added
        new_records = []
        for row in csv_data:
            if row['name'] not in existing_names:
                new_records.append(Dummy(name=row['name'], marks=row['marks']))
        
        # Bulk create new records
        if new_records:
            Dummy.objects.bulk_create(new_records)


def staff_add_result_test1_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_add_result_test1')
    else:
        student_admin_id = request.POST.get('student_list')
        exam_marks = request.POST.get('exam_marks')
        subject_id = request.POST.get('subject')

        student_obj = Students.objects.get(admin=student_admin_id)
        subject_obj = Subjects.objects.get(id=subject_id)

        try:
            # Check if Students Result Already Exists or not
            check_exist = StudentResult.objects.filter(subject_id=subject_obj, student_id=student_obj).exists()
            if check_exist:
                result = StudentResult.objects.get(subject_id=subject_obj, student_id=student_obj)
                result.test1_marks = exam_marks
                result.total_CA = float(result.test1_marks) + float(result.test2_marks) + float(result.UE_marks)
                result.save()
                messages.success(request, "Result Updated Successfully!")
                return redirect('staff_add_result_test1')
            else:
                result = StudentResult(student_id=student_obj, subject_id=subject_obj, test1_marks=exam_marks)
                result.save()
                messages.success(request, "Result Added Successfully!")
                return redirect('staff_add_result_test1')
        except Exception as e:
            messages.error(request, "Failed to Add Result!")
            print(e)
            return redirect('staff_add_result_test1')