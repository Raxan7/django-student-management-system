from .models import *
from.ml_model import load_model

def make_general_predictions(student_obj, subject_id):
    students = Students.objects.filter(admin=student_obj)
    for student in students:
        try:
            student_result = StudentResult.objects.get(student_id=student.id, subject_id=subject_id)
            student_data = StudentPerformance.objects.get(student=student)
            test1, test2 = student_result.test1_marks, student_result.test2_marks
            dataset = [
                student_data.age, student_data.medu, student_data.fedu, student_data.traveltime, student_data.studytime,
                student_data.failures, student_data.famrel, student_data.freetime, student_data.goout, 
                student_data.dalc, student_data.walc, student_data.health, student_data.absences, 
                test1, test2
            ]
            results = load_model().predict([dataset])
            results = round(results[0] / 20 * 60, 2)
            total = float(test1) + float(test2) + float(results)
            try:
                # Check if Students Result Already Exists or not
                check_exist = PredictionModel.objects.filter(exam__student_id__id=student.id,
                                                             exam__subject_id__id=subject_id).exists()
                if check_exist:
                    prediction_obj = PredictionModel.objects.get(exam__student_id__id=student.id,
                                                                    exam__subject_id__id=subject_id)
                    prediction_obj.test1_marks = test1
                    prediction_obj.test2_marks = test2
                    prediction_obj.UE_prediction = results
                    prediction_obj.total_CA = total
                    prediction_obj.save()
                else:

                    existing_obj = PredictionModel(
                        exam=student_result,
                        test1_marks=test1,
                        test2_marks=test2,
                        UE_prediction=results,
                        total_CA=total
                    )
                    existing_obj.save()
                print("Successfully Predicted")
            except Exception as i:
                print(i)
        except Exception as e:
            print(e)
