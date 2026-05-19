from decimal import Decimal
from django.db.models import Avg, Sum, Q
from django.utils import timezone

from apps.accounts.models import StudentProfile
from apps.academic.models import Semester, AcademicRecord
from apps.attendance.models import AttendanceSummary
from apps.assignments.models import AssignmentScore
from apps.activities.models import ActivityScore
from apps.evaluations.models import TutorEvaluation, DisciplineRecord
from apps.penalties.models import PenaltySummary
from .models import GrantScore, EmploymentRecord


class GrantScoringService:
    """Core service for calculating grant scores"""

    @staticmethod
    def calculate_student_score(student: StudentProfile, semester: Semester) -> GrantScore:
        score, _ = GrantScore.objects.get_or_create(student=student, semester=semester)

        # 1. Academic (40 pts)
        avg_gpa = AcademicRecord.objects.filter(
            student=student, semester=semester,
        ).aggregate(avg=Avg("grade_percentage"))["avg"]
        gpa = float(avg_gpa) if avg_gpa else 0
        score.gpa_percentage = Decimal(str(gpa))
        score.academic_score = Decimal(str(min((gpa / 100) * 40, 40)))
        score.gpa_eligible = gpa >= 80

        # 2. Attendance (20 pts)
        att = AttendanceSummary.objects.filter(student=student, semester=semester).first()
        score.attendance_score = Decimal(str(att.score)) if att else Decimal("0")

        # 3. Assignments (15 pts)
        asn = AssignmentScore.objects.filter(student=student, semester=semester).first()
        score.assignment_score = Decimal(str(asn.score)) if asn else Decimal("0")

        # 4. Activities (10 pts)
        act = ActivityScore.objects.filter(student=student, semester=semester).first()
        score.activity_score = Decimal(str(act.total_score)) if act else Decimal("0")

        # 5. Tutor (5 pts)
        tutor_avg = TutorEvaluation.objects.filter(
            student=student, semester=semester,
        ).aggregate(avg=Avg("total_score"))["avg"]
        score.tutor_score = Decimal(str(min(float(tutor_avg), 5))) if tutor_avg else Decimal("0")

        # 6. Discipline (10 pts)
        disc = DisciplineRecord.objects.filter(student=student, semester=semester).first()
        score.discipline_score = Decimal(str(disc.score)) if disc else Decimal("10")

        # 7. Penalty & Recovery
        pen = PenaltySummary.objects.filter(student=student, semester=semester).first()
        if pen:
            score.penalty_score = pen.total_penalty
            score.recovery_score = pen.total_recovery
        else:
            score.penalty_score = Decimal("0")
            score.recovery_score = Decimal("0")

        # 8. Employment (bonus 10 pts)
        emp = EmploymentRecord.objects.filter(
            student=student, semester=semester, status="approved",
        ).aggregate(total=Sum("score"))["total"]
        score.employment_score = Decimal(str(min(float(emp), 10))) if emp else Decimal("0")

        score.calculate_total()
        score.status = GrantScore.Status.CALCULATED
        score.calculated_at = timezone.now()
        score.save()

        return score

    @staticmethod
    def calculate_all_scores(semester: Semester) -> int:
        students = StudentProfile.objects.filter(
            Q(status=StudentProfile.Status.GRANT) | Q(grant_status=StudentProfile.GrantStatus.ACTIVE)
        )
        count = 0
        for student in students:
            GrantScoringService.calculate_student_score(student, semester)
            count += 1

        GrantScoringService.update_rankings(semester)
        return count

    @staticmethod
    def update_rankings(semester: Semester):
        scores = GrantScore.objects.filter(semester=semester).order_by("-final_score")
        for rank, score in enumerate(scores, 1):
            score.rank = rank
            score.save(update_fields=["rank"])

    @staticmethod
    def get_grant_eligible(semester: Semester, min_score: float = 80):
        return GrantScore.objects.filter(
            semester=semester,
            final_score__gte=min_score,
            gpa_eligible=True,
        ).order_by("-final_score")

    @staticmethod
    def get_rating_table(semester: Semester):
        return GrantScore.objects.filter(
            semester=semester,
        ).select_related("student__user").order_by("rank")
