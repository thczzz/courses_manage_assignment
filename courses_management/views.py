import csv
from io import BytesIO
from datetime import datetime
from django.shortcuts import render
from django.db.models import Sum
from django.http import FileResponse, HttpResponse
from .models import Student


def index(request):
    if request.method == "GET":
        min_credits = request.GET.get("min_credits")
        if min_credits:
            min_credits = int(min_credits)
            student_pins = []
            pins = request.GET.get("student_pins")
            pins_filter = {}
            if pins != "":
                student_pins = pins.strip().split(',')
                pins_filter = {"pin__in": student_pins}
            start_date = datetime.strptime(request.GET.get("start_date"), '%Y-%m-%d')
            end_date = datetime.strptime(request.GET.get("end_date"), '%Y-%m-%d')
            output_format = request.GET.get("output_format")

            eligible_students = Student.objects.filter(
                student_courses_xref__completion_date__range=(start_date, end_date), **pins_filter).annotate(
                total_credits=Sum("student_courses_xref__course__credit")
            ).filter(total_credits__gte=min_credits).distinct()

            ready_data = {}
            for student in eligible_students:
                courses = student.student_courses_xref_set.filter(completion_date__range=(start_date, end_date)).values(
                    "course__name", "course__total_time", "course__credit",
                    "course__instructor__first_name", "course__instructor__last_name"
                )
                ready_data[(student.pin, student.first_name, student.last_name, student.total_credits)] = courses

            if output_format == ".html":
                response = render(request, "report.html", {"ready_data": ready_data})
                f = BytesIO(response.content)
                return FileResponse(f, as_attachment=True, filename="report.html")

            elif output_format == ".csv":
                response = HttpResponse(
                    content_type='text/csv',
                    headers={'Content-Disposition': 'attachment; filename="report.csv"'},
                )
                writer = csv.writer(response)
                writer.writerow(['Student', 'Total Credits', 'Course', 'Credit', 'Time', 'Instructor'])
                for student_info, courses in ready_data.items():
                    counter = 0
                    for course in courses:
                        writer.writerow(
                            [
                                f"{student_info[1]} {student_info[2]}" if counter == 0 else '',
                                student_info[3] if counter == 0 else '',
                                course["course__name"],
                                course["course__credit"],
                                course["course__total_time"],
                                f"{course['course__instructor__first_name']} {course['course__instructor__last_name']}"
                            ]
                        )
                        counter += 1
                return response

    return render(request, "index.html", {})
