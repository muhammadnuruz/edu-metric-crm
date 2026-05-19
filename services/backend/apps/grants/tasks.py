from celery import shared_task
from apps.academic.models import Semester
from .services import GrantScoringService


@shared_task
def calculate_all_grant_scores(semester_id: int) -> dict:
    semester = Semester.objects.get(id=semester_id)
    count = GrantScoringService.calculate_all_scores(semester)
    return {"semester": str(semester), "students_processed": count}


@shared_task
def calculate_student_grant_score(student_id: int, semester_id: int) -> dict:
    from apps.accounts.models import StudentProfile
    student = StudentProfile.objects.get(id=student_id)
    semester = Semester.objects.get(id=semester_id)
    score = GrantScoringService.calculate_student_score(student, semester)
    return {
        "student": str(student),
        "final_score": float(score.final_score),
        "rank": score.rank,
    }
