import random
from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import User, StudentProfile
from apps.academic.models import Semester, Subject, AcademicRecord
from apps.attendance.models import AttendanceRecord, AttendanceSummary
from apps.assignments.models import Assignment, AssignmentSubmission, AssignmentScore
from apps.activities.models import Activity, ActivityScore
from apps.evaluations.models import TutorEvaluation, MentorFeedback, DisciplineRecord
from apps.penalties.models import Penalty, Recovery, PenaltySummary
from apps.grants.models import GrantScore, EmploymentRecord
from apps.grants.services import GrantScoringService


PASSWORD = "test1234"


class Command(BaseCommand):
    help = "Seed database with mock data for all roles"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        admin = self._create_user("admin", "Admin", "Rahimov", "admin")
        teacher1 = self._create_user("teacher1", "Jamshid", "Karimov", "teacher")
        teacher2 = self._create_user("teacher2", "Nodira", "Aliyeva", "teacher")
        tutor1 = self._create_user("tutor1", "Sardor", "Toshmatov", "tutor")
        tutor2 = self._create_user("tutor2", "Malika", "Yusupova", "tutor")
        parent1 = self._create_user("parent1", "Anvar", "Raximov", "parent")
        parent2 = self._create_user("parent2", "Gulnora", "Nazarova", "parent")

        semester = self._create_semester()
        subjects = self._create_subjects(semester, teacher1, teacher2)

        students_data = [
            ("student1", "Aziz", "Raximov", "SE-101", 1, "grant", parent1, teacher1, tutor1),
            ("student2", "Dilshod", "Usmonov", "SE-101", 1, "grant", parent2, teacher1, tutor1),
            ("student3", "Shahlo", "Qodirova", "SE-102", 1, "contract", None, teacher2, tutor2),
            ("student4", "Bekzod", "Xolmatov", "SE-102", 1, "grant", None, teacher2, tutor2),
            ("student5", "Kamola", "Ergasheva", "SE-101", 1, "contract", None, teacher1, tutor1),
            ("student6", "Otabek", "Mirzayev", "CS-201", 2, "grant", parent1, teacher2, tutor2),
            ("student7", "Zarina", "Abdullayeva", "CS-201", 2, "grant", parent2, teacher2, tutor1),
            ("student8", "Farrux", "Ismoilov", "CS-202", 2, "contract", None, teacher1, tutor2),
            ("student9", "Nilufar", "Karimova", "CS-202", 2, "grant", None, teacher1, tutor1),
            ("student10", "Jasur", "Sobirov", "SE-101", 1, "grant", None, teacher2, tutor2),
        ]

        students = []
        for idx, (uname, fn, ln, group, course, status, parent, mentor, tutor) in enumerate(students_data, 1):
            user = self._create_user(uname, fn, ln, "student")
            sid = f"PDP-2026-{idx:03d}"
            profile, _ = StudentProfile.objects.get_or_create(
                user=user,
                defaults={
                    "student_id": sid,
                    "group": group,
                    "course": course,
                    "semester": semester.semester_number,
                    "status": status,
                    "grant_status": "active",
                    "enrollment_date": date(2025, 9, 1),
                    "mentor": mentor,
                    "tutor": tutor,
                    "parent": parent,
                },
            )
            students.append(profile)

        self._create_academic_records(students, subjects, semester)
        self._create_attendance(students, subjects, semester, teacher1)
        self._create_assignments(students, subjects, semester, teacher1, teacher2)
        self._create_activities(students, semester, admin)
        self._create_evaluations(students, semester, tutor1, tutor2, teacher1, teacher2)
        self._create_penalties(students, semester, admin)
        self._create_employment(students, semester)

        self.stdout.write("Calculating grant scores...")
        GrantScoringService.calculate_all_scores(semester)

        self.stdout.write(self.style.SUCCESS("\n=== LOGIN MA'LUMOTLARI ==="))
        self.stdout.write(self.style.SUCCESS(f"Parol (hammasi uchun): {PASSWORD}"))
        self.stdout.write("")
        accounts = [
            ("admin", "Admin", "Admin Rahimov"),
            ("teacher1", "Teacher/Mentor", "Jamshid Karimov"),
            ("teacher2", "Teacher/Mentor", "Nodira Aliyeva"),
            ("tutor1", "Tutor", "Sardor Toshmatov"),
            ("tutor2", "Tutor", "Malika Yusupova"),
            ("parent1", "Parent", "Anvar Raximov"),
            ("parent2", "Parent", "Gulnora Nazarova"),
            ("student1", "Student", "Aziz Raximov"),
            ("student2", "Student", "Dilshod Usmonov"),
            ("student3", "Student", "Shahlo Qodirova"),
            ("student4", "Student", "Bekzod Xolmatov"),
            ("student5", "Student", "Kamola Ergasheva"),
            ("student6", "Student", "Otabek Mirzayev"),
            ("student7", "Student", "Zarina Abdullayeva"),
            ("student8", "Student", "Farrux Ismoilov"),
            ("student9", "Student", "Nilufar Karimova"),
            ("student10", "Student", "Jasur Sobirov"),
        ]
        self.stdout.write(f"{'Username':<12} {'Role':<16} {'Ism':<25}")
        self.stdout.write("-" * 55)
        for uname, role, name in accounts:
            self.stdout.write(f"{uname:<12} {role:<16} {name:<25}")

    def _create_user(self, username, first_name, last_name, role):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
                "email": f"{username}@pdp.uz",
                "phone": f"+99890{random.randint(1000000, 9999999)}",
                "is_staff": role == "admin",
                "is_superuser": role == "admin",
            },
        )
        if created:
            user.set_password(PASSWORD)
            user.save()
        return user

    def _create_semester(self):
        semester, _ = Semester.objects.get_or_create(
            year=2026,
            semester_number=1,
            defaults={
                "name": "2025-2026 1-semestr",
                "start_date": date(2025, 9, 1),
                "end_date": date(2026, 1, 31),
                "is_active": True,
            },
        )
        return semester

    def _create_subjects(self, semester, teacher1, teacher2):
        subjects_data = [
            ("CS101", "Python dasturlash", 1, teacher1),
            ("CS102", "Web dasturlash", 1, teacher2),
            ("CS103", "Ma'lumotlar tuzilmasi", 1, teacher1),
            ("CS201", "Algoritmlar", 2, teacher2),
            ("CS202", "Databaza", 2, teacher1),
        ]
        subjects = []
        for code, name, course, teacher in subjects_data:
            subj, _ = Subject.objects.get_or_create(
                code=code,
                defaults={
                    "name": name,
                    "course": course,
                    "semester": semester,
                    "teacher": teacher,
                },
            )
            subjects.append(subj)
        return subjects

    def _create_academic_records(self, students, subjects, semester):
        for student in students:
            course_subjects = [s for s in subjects if s.course == student.course]
            for subject in course_subjects:
                grade = random.uniform(55, 100)
                AcademicRecord.objects.get_or_create(
                    student=student,
                    subject=subject,
                    semester=semester,
                    defaults={"grade_percentage": Decimal(str(round(grade, 2)))},
                )

    def _create_attendance(self, students, subjects, semester, teacher):
        for student in students:
            course_subjects = [s for s in subjects if s.course == student.course]
            for subject in course_subjects:
                total = random.randint(25, 35)
                for i in range(total):
                    day = date(2025, 9, 1) + timedelta(days=i * 2)
                    status = random.choices(
                        ["present", "present", "present", "late", "absent", "excused"],
                        weights=[60, 20, 10, 5, 3, 2],
                    )[0]
                    AttendanceRecord.objects.get_or_create(
                        student=student,
                        subject=subject,
                        date=day,
                        defaults={
                            "semester": semester,
                            "status": status,
                            "recorded_by": teacher,
                        },
                    )

            summary, _ = AttendanceSummary.objects.get_or_create(
                student=student,
                semester=semester,
            )
            summary.recalculate()

    def _create_assignments(self, students, subjects, semester, teacher1, teacher2):
        for subject in subjects:
            for i in range(3):
                atype = ["homework", "project", "lab"][i]
                assignment, _ = Assignment.objects.get_or_create(
                    title=f"{subject.name} - {atype.capitalize()} {i+1}",
                    subject=subject,
                    semester=semester,
                    defaults={
                        "assignment_type": atype,
                        "deadline": timezone.now() + timedelta(days=30),
                        "created_by": subject.teacher,
                    },
                )

                for student in students:
                    if subject.course != student.course:
                        continue
                    quality = random.choice(["excellent", "good", "good", "average", "poor"])
                    score = {"excellent": 95, "good": 80, "average": 65, "poor": 40}[quality]
                    AssignmentSubmission.objects.get_or_create(
                        assignment=assignment,
                        student=student,
                        defaults={
                            "quality": quality,
                            "score": Decimal(str(score + random.randint(-5, 5))),
                            "is_independent": random.random() > 0.15,
                            "is_late": random.random() < 0.1,
                            "graded_by": subject.teacher,
                            "graded_at": timezone.now(),
                        },
                    )

        for student in students:
            ascore, _ = AssignmentScore.objects.get_or_create(
                student=student,
                semester=semester,
            )
            ascore.recalculate()

    def _create_activities(self, students, semester, admin):
        categories = [
            ("competition", "ACM ICPC Regional", 3),
            ("startup", "EduTech Startup loyihasi", 5),
            ("cert_pdp", "PDP Backend sertifikat", 3),
            ("cert_international", "AWS Cloud Practitioner", 8),
            ("cert_language", "IELTS 7.0", 5),
            ("volunteering", "IT Volunteer dasturi", 2),
            ("mentoring", "Junior mentorlik", 3),
            ("soft_skills", "Leadership training", 1),
            ("networking", "Tech meetup tashkilotchisi", 1),
            ("project_participant", "Open source loyiha", 2),
            ("direction_assistant", "Yo'nalish asistenti", 3),
        ]

        for student in students:
            num_activities = random.randint(1, 5)
            chosen = random.sample(categories, min(num_activities, len(categories)))
            for category, title, score in chosen:
                status = random.choices(
                    ["approved", "approved", "pending", "rejected"],
                    weights=[50, 30, 15, 5],
                )[0]
                Activity.objects.get_or_create(
                    student=student,
                    semester=semester,
                    category=category,
                    title=title,
                    defaults={
                        "description": f"{title} - {student.user.get_full_name()} tomonidan",
                        "score": Decimal(str(score)) if status == "approved" else Decimal("0"),
                        "status": status,
                        "verified_by": admin if status != "pending" else None,
                        "verified_at": timezone.now() if status != "pending" else None,
                        "proof_url": f"https://example.com/proof/{student.student_id}",
                    },
                )

            ascore, _ = ActivityScore.objects.get_or_create(
                student=student,
                semester=semester,
            )
            ascore.recalculate()

    def _create_evaluations(self, students, semester, tutor1, tutor2, teacher1, teacher2):
        for student in students:
            tutor = student.tutor or tutor1
            TutorEvaluation.objects.get_or_create(
                student=student,
                semester=semester,
                evaluator=tutor,
                defaults={
                    "corporate_culture": Decimal(str(random.choice([0, 0.5, 1]))),
                    "social_activity": Decimal(str(random.choice([0, 0.5, 1]))),
                    "soft_skills": Decimal(str(random.choice([0, 0.5, 1]))),
                    "discipline": Decimal(str(random.choice([0, 0.5, 1]))),
                    "dormitory": Decimal(str(random.choice([0, 0.5, 1]))),
                    "comment": "Umumiy baholash",
                },
            )

            mentor = student.mentor or teacher1
            MentorFeedback.objects.get_or_create(
                student=student,
                semester=semester,
                mentor=mentor,
                defaults={
                    "technical_skills": random.choice(["excellent", "good", "average"]),
                    "participation": random.choice(["excellent", "good", "average"]),
                    "teamwork": random.choice(["excellent", "good", "average"]),
                    "initiative": random.choice(["excellent", "good", "average", "below_average"]),
                    "overall_comment": f"{student.user.get_full_name()} bo'yicha mentor bahosi",
                },
            )

            DisciplineRecord.objects.get_or_create(
                student=student,
                semester=semester,
                defaults={
                    "academic_honesty": Decimal(str(random.randint(6, 10))),
                    "recorded_by": tutor,
                },
            )

    def _create_penalties(self, students, semester, admin):
        penalty_data = [
            ("light", "late", -1, "Darsga kechikish"),
            ("light", "phone", -1, "Dars vaqtida telefon"),
            ("medium", "absent", -3, "Sababsiz dars qoldirish"),
            ("medium", "dormitory", -3, "Yotoqxona qoidalari buzilishi"),
            ("heavy", "cheating", -10, "Imtihonda ko'chirish"),
        ]

        for student in students:
            if random.random() < 0.4:
                continue
            num_penalties = random.randint(1, 3)
            for _ in range(num_penalties):
                sev, cat, pts, desc = random.choice(penalty_data)
                Penalty.objects.create(
                    student=student,
                    semester=semester,
                    severity=sev,
                    category=cat,
                    points=Decimal(str(pts)),
                    description=desc,
                    issued_by=admin,
                )

            if random.random() < 0.5:
                Recovery.objects.create(
                    student=student,
                    semester=semester,
                    task_description="Qo'shimcha vazifa bajarish: kutubxonada 10 soat ishlash",
                    recovery_points=Decimal(str(random.randint(1, 5))),
                    status="completed",
                    assigned_by=admin,
                    completed_at=timezone.now(),
                )

            summary, _ = PenaltySummary.objects.get_or_create(
                student=student,
                semester=semester,
            )
            summary.recalculate()

    def _create_employment(self, students, semester):
        companies = [
            ("EPAM Systems", "Junior Developer", "internship", 4),
            ("Uzum", "Backend Intern", "internship", 3),
            ("Najot Ta'lim", "Part-time Mentor", "part_time", 6),
            ("Google", "SWE Intern", "internship", 5),
            ("PDP Academy", "Lab Assistant", "part_time", 5),
        ]

        for student in students:
            if random.random() < 0.5:
                continue
            company, position, etype, score = random.choice(companies)
            EmploymentRecord.objects.get_or_create(
                student=student,
                semester=semester,
                defaults={
                    "employment_type": etype,
                    "company_name": company,
                    "position": position,
                    "start_date": date(2025, 10, 1),
                    "score": Decimal(str(score)),
                    "status": random.choice(["approved", "approved", "pending"]),
                    "proof_url": f"https://example.com/employment/{student.student_id}",
                },
            )
