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

UZBEK_FIRST_NAMES_M = [
    "Aziz", "Dilshod", "Bekzod", "Otabek", "Farrux", "Jasur", "Sardor",
    "Sherzod", "Islom", "Asilbek", "Doniyor", "Mirzo", "Sanjar", "Bobur",
    "Alisher", "Nodir", "Kamol", "Ulugbek", "Temur", "Behruz", "Javohir",
    "Abror", "Eldor", "Humoyun", "Firdavs",
]
UZBEK_FIRST_NAMES_F = [
    "Shahlo", "Kamola", "Zarina", "Nilufar", "Malika", "Nodira", "Gulnora",
    "Madina", "Fotima", "Dildora", "Sevinch", "Mohira", "Lobar", "Iroda",
    "Dilnoza", "Nasiba", "Feruza", "Ozoda", "Shaxlo", "Barno", "Nargiza",
    "Munira", "Hilola", "Zilola", "Sabina",
]
UZBEK_LAST_NAMES = [
    "Raximov", "Usmonov", "Qodirova", "Xolmatov", "Ergasheva", "Mirzayev",
    "Abdullayeva", "Ismoilov", "Karimova", "Sobirov", "Toshmatov", "Yusupova",
    "Nazarova", "Aliyeva", "Karimov", "Rahimov", "Tursunov", "Xasanov",
    "Jumayev", "Normatov", "Salimov", "Bobojonov", "Murodov", "Halimov",
    "Qodirov", "Rustamov", "Sharipov", "Umarov", "Yunusov", "Zakirov",
]


class Command(BaseCommand):
    help = "Seed database with comprehensive mock data for all roles"

    def handle(self, *args, **options):
        self.stdout.write("Clearing old data...")
        self._clear_data()

        self.stdout.write("Seeding database with comprehensive mock data...")

        admin = self._create_user("admin", "Admin", "Rahimov", "admin", "+998901234567", "11111111111111")
        teacher1 = self._create_user("teacher1", "Jamshid", "Karimov", "teacher", "+998901112233")
        teacher2 = self._create_user("teacher2", "Nodira", "Aliyeva", "teacher", "+998901112244")
        teacher3 = self._create_user("teacher3", "Rustam", "Tursunov", "teacher", "+998901112255")
        tutor1 = self._create_user("tutor1", "Sardor", "Toshmatov", "tutor", "+998901113311")
        tutor2 = self._create_user("tutor2", "Malika", "Yusupova", "tutor", "+998901113322")
        komendant1 = self._create_user("komendant1", "Bahrom", "Xasanov", "komendant", "+998901114411")
        komendant2 = self._create_user("komendant2", "Dilorom", "Jumayeva", "komendant", "+998901114422")
        manager1 = self._create_user("manager1", "Timur", "Normatov", "manager", "+998901115511")
        parent1 = self._create_user("parent1", "Anvar", "Raximov", "parent", "+998901116611")
        parent2 = self._create_user("parent2", "Gulnora", "Nazarova", "parent", "+998901116622")
        parent3 = self._create_user("parent3", "Oybek", "Salimov", "parent", "+998901116633")
        parent4 = self._create_user("parent4", "Manzura", "Bobojonova", "parent", "+998901116644")

        semester = self._create_semester()
        subjects = self._create_subjects(semester, teacher1, teacher2, teacher3)

        groups_1 = ["SE-101", "SE-102", "SE-103"]
        groups_2 = ["CS-201", "CS-202"]
        groups_3 = ["AI-301"]
        teachers = [teacher1, teacher2, teacher3]
        tutors = [tutor1, tutor2]
        parents = [parent1, parent2, parent3, parent4, None, None, None]

        students_data = []
        pnfl_counter = 20000000000000
        student_counter = 0
        for group in groups_1:
            for i in range(8):
                student_counter += 1
                is_female = random.random() < 0.4
                fn = random.choice(UZBEK_FIRST_NAMES_F if is_female else UZBEK_FIRST_NAMES_M)
                ln = random.choice(UZBEK_LAST_NAMES)
                if is_female and not ln.endswith("a"):
                    ln += "a"
                pnfl_counter += random.randint(1, 100)
                students_data.append((
                    f"student{student_counter}", fn, ln, group, 1, 1,
                    random.choice(["grant", "grant", "contract"]),
                    random.choice(parents),
                    random.choice(teachers),
                    random.choice(tutors),
                    str(pnfl_counter),
                ))

        for group in groups_2:
            for i in range(7):
                student_counter += 1
                is_female = random.random() < 0.4
                fn = random.choice(UZBEK_FIRST_NAMES_F if is_female else UZBEK_FIRST_NAMES_M)
                ln = random.choice(UZBEK_LAST_NAMES)
                if is_female and not ln.endswith("a"):
                    ln += "a"
                pnfl_counter += random.randint(1, 100)
                students_data.append((
                    f"student{student_counter}", fn, ln, group, 2, 3,
                    random.choice(["grant", "grant", "contract"]),
                    random.choice(parents),
                    random.choice(teachers),
                    random.choice(tutors),
                    str(pnfl_counter),
                ))

        for group in groups_3:
            for i in range(5):
                student_counter += 1
                is_female = random.random() < 0.4
                fn = random.choice(UZBEK_FIRST_NAMES_F if is_female else UZBEK_FIRST_NAMES_M)
                ln = random.choice(UZBEK_LAST_NAMES)
                if is_female and not ln.endswith("a"):
                    ln += "a"
                pnfl_counter += random.randint(1, 100)
                students_data.append((
                    f"student{student_counter}", fn, ln, group, 3, 5,
                    random.choice(["grant", "contract"]),
                    random.choice(parents),
                    random.choice(teachers),
                    random.choice(tutors),
                    str(pnfl_counter),
                ))

        students = []
        for idx, (uname, fn, ln, group, course, sem, status, parent, mentor, tutor, pnfl) in enumerate(students_data, 1):
            user = self._create_user(uname, fn, ln, "student", pnfl=pnfl)
            sid = f"PDP-2026-{idx:03d}"
            profile, _ = StudentProfile.objects.get_or_create(
                user=user,
                defaults={
                    "student_id": sid,
                    "group": group,
                    "course": course,
                    "semester": sem,
                    "status": status,
                    "grant_status": "active",
                    "enrollment_date": date(2025, 9, 1),
                    "mentor": mentor,
                    "tutor": tutor,
                    "parent": parent,
                },
            )
            students.append(profile)

        self.stdout.write(f"  Created {len(students)} students")

        self._create_academic_records(students, subjects, semester)
        self._create_attendance(students, subjects, semester, teachers)
        self._create_assignments(students, subjects, semester, teachers)
        self._create_activities(students, semester, admin)
        self._create_evaluations(students, semester, [tutor1, tutor2], [komendant1, komendant2], manager1, teachers)
        self._create_penalties(students, semester, admin, [tutor1, tutor2], [komendant1, komendant2])
        self._create_employment(students, semester)

        self.stdout.write("Calculating grant scores...")
        GrantScoringService.calculate_all_scores(semester)

        self.stdout.write(self.style.SUCCESS("\n" + "=" * 65))
        self.stdout.write(self.style.SUCCESS("  LOGIN MA'LUMOTLARI"))
        self.stdout.write(self.style.SUCCESS("=" * 65))
        self.stdout.write(self.style.SUCCESS(f"  Parol (hammasi uchun): {PASSWORD}"))
        self.stdout.write("")
        accounts = [
            ("admin", "Admin", "Admin Rahimov"),
            ("teacher1", "Teacher", "Jamshid Karimov"),
            ("teacher2", "Teacher", "Nodira Aliyeva"),
            ("teacher3", "Teacher", "Rustam Tursunov"),
            ("tutor1", "Tutor", "Sardor Toshmatov"),
            ("tutor2", "Tutor", "Malika Yusupova"),
            ("komendant1", "Komendant", "Bahrom Xasanov"),
            ("komendant2", "Komendant", "Dilorom Jumayeva"),
            ("manager1", "Unicron Mgr", "Timur Normatov"),
            ("parent1", "Parent", "Anvar Raximov (+998901116611)"),
            ("parent2", "Parent", "Gulnora Nazarova (+998901116622)"),
            ("parent3", "Parent", "Oybek Salimov (+998901116633)"),
            ("parent4", "Parent", "Manzura Bobojonova (+998901116644)"),
        ]
        self.stdout.write(f"  {'Username':<14} {'Role':<14} {'Ism':<35}")
        self.stdout.write("  " + "-" * 63)
        for uname, role, name in accounts:
            self.stdout.write(f"  {uname:<14} {role:<14} {name:<35}")

        self.stdout.write("")
        self.stdout.write(f"  {'student1-student{0}'.format(len(students)):<14} {'Student':<14} {len(students)} ta talaba")
        self.stdout.write("  " + "-" * 63)
        self.stdout.write(self.style.SUCCESS(f"\n  Jami: {len(students)} talaba, {len(subjects)} fan, 6 ta guruh"))
        self.stdout.write(self.style.SUCCESS("=" * 65))

    def _clear_data(self):
        GrantScore.objects.all().delete()
        EmploymentRecord.objects.all().delete()
        PenaltySummary.objects.all().delete()
        Recovery.objects.all().delete()
        Penalty.objects.all().delete()
        DisciplineRecord.objects.all().delete()
        MentorFeedback.objects.all().delete()
        TutorEvaluation.objects.all().delete()
        ActivityScore.objects.all().delete()
        Activity.objects.all().delete()
        AssignmentScore.objects.all().delete()
        AssignmentSubmission.objects.all().delete()
        Assignment.objects.all().delete()
        AttendanceSummary.objects.all().delete()
        AttendanceRecord.objects.all().delete()
        AcademicRecord.objects.all().delete()
        Subject.objects.all().delete()
        Semester.objects.all().delete()
        StudentProfile.objects.all().delete()
        User.objects.all().delete()

    def _create_user(self, username, first_name, last_name, role, phone=None, pnfl=None):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
                "email": f"{username}@pdp.uz",
                "phone": phone or f"+99890{random.randint(1000000, 9999999)}",
                "pnfl": pnfl,
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

    def _create_subjects(self, semester, teacher1, teacher2, teacher3):
        subjects_data = [
            ("CS101", "Python dasturlash", 1, teacher1),
            ("CS102", "Web dasturlash", 1, teacher2),
            ("CS103", "Ma'lumotlar tuzilmasi", 1, teacher3),
            ("CS104", "Diskret matematika", 1, teacher1),
            ("CS201", "Algoritmlar", 2, teacher2),
            ("CS202", "Databaza", 2, teacher1),
            ("CS203", "Operatsion tizimlar", 2, teacher3),
            ("CS204", "Kompyuter tarmoqlari", 2, teacher2),
            ("AI301", "Sun'iy intellekt asoslari", 3, teacher3),
            ("AI302", "Machine Learning", 3, teacher1),
            ("AI303", "Deep Learning", 3, teacher2),
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
        self.stdout.write("  Creating academic records...")
        for student in students:
            course_subjects = [s for s in subjects if s.course == student.course]
            for subject in course_subjects:
                grade = random.gauss(75, 12)
                grade = max(40, min(100, grade))
                AcademicRecord.objects.get_or_create(
                    student=student,
                    subject=subject,
                    semester=semester,
                    defaults={"grade_percentage": Decimal(str(round(grade, 2)))},
                )

    def _create_attendance(self, students, subjects, semester, teachers):
        self.stdout.write("  Creating attendance records...")
        for student in students:
            course_subjects = [s for s in subjects if s.course == student.course]
            for subject in course_subjects:
                total = random.randint(28, 40)
                for i in range(total):
                    day = date(2025, 9, 1) + timedelta(days=i * 2)
                    if day.weekday() >= 5:
                        continue
                    status = random.choices(
                        ["present", "present", "present", "late", "absent", "excused"],
                        weights=[55, 20, 10, 8, 5, 2],
                    )[0]
                    AttendanceRecord.objects.get_or_create(
                        student=student,
                        subject=subject,
                        date=day,
                        defaults={
                            "semester": semester,
                            "status": status,
                            "recorded_by": random.choice(teachers),
                        },
                    )

            summary, _ = AttendanceSummary.objects.get_or_create(
                student=student,
                semester=semester,
            )
            summary.recalculate()

    def _create_assignments(self, students, subjects, semester, teachers):
        self.stdout.write("  Creating assignments...")
        for subject in subjects:
            for i in range(4):
                atype = ["homework", "project", "lab", "homework"][i]
                assignment, _ = Assignment.objects.get_or_create(
                    title=f"{subject.name} - {atype.capitalize()} {i+1}",
                    subject=subject,
                    semester=semester,
                    defaults={
                        "assignment_type": atype,
                        "deadline": timezone.now() + timedelta(days=random.randint(7, 60)),
                        "created_by": subject.teacher,
                    },
                )

                for student in students:
                    if subject.course != student.course:
                        continue
                    if random.random() < 0.05:
                        continue
                    quality = random.choices(
                        ["excellent", "good", "average", "poor"],
                        weights=[20, 40, 30, 10],
                    )[0]
                    score = {"excellent": 95, "good": 80, "average": 65, "poor": 40}[quality]
                    AssignmentSubmission.objects.get_or_create(
                        assignment=assignment,
                        student=student,
                        defaults={
                            "quality": quality,
                            "score": Decimal(str(max(0, min(100, score + random.randint(-8, 8))))),
                            "is_independent": random.random() > 0.12,
                            "is_late": random.random() < 0.08,
                            "graded_by": subject.teacher,
                            "graded_at": timezone.now() - timedelta(days=random.randint(0, 30)),
                        },
                    )

        for student in students:
            ascore, _ = AssignmentScore.objects.get_or_create(
                student=student,
                semester=semester,
            )
            ascore.recalculate()

    def _create_activities(self, students, semester, admin):
        self.stdout.write("  Creating activities...")
        categories = [
            ("competition", "ACM ICPC Regional", 3),
            ("competition", "Google Code Jam", 3),
            ("startup", "EduTech Startup loyihasi", 5),
            ("startup", "FinTech MVP", 7),
            ("cert_pdp", "PDP Backend sertifikat", 3),
            ("cert_pdp", "PDP Frontend sertifikat", 3),
            ("cert_international", "AWS Cloud Practitioner", 8),
            ("cert_international", "Google Cloud Associate", 10),
            ("cert_national", "Milliy IT sertifikat", 2),
            ("cert_language", "IELTS 7.0", 5),
            ("cert_language", "CEFR B2 Ingliz tili", 3),
            ("volunteering", "IT Volunteer dasturi", 2),
            ("volunteering", "Xayriya tadbiri", 2),
            ("mentoring", "Junior mentorlik", 3),
            ("mentoring", "Bootcamp mentorlik", 3),
            ("soft_skills", "Leadership training", 1),
            ("soft_skills", "Public speaking workshop", 1),
            ("networking", "Tech meetup tashkilotchisi", 1),
            ("project_participant", "Open source loyiha", 2),
            ("project_participant", "Hackathon ishtirokchisi", 2),
            ("direction_assistant", "Yo'nalish asistenti", 3),
            ("strategic_assistant", "Strategik yordamchi", 4),
        ]

        for student in students:
            num_activities = random.randint(2, 7)
            chosen = random.sample(categories, min(num_activities, len(categories)))
            for category, title, score in chosen:
                status = random.choices(
                    ["approved", "approved", "approved", "pending", "rejected"],
                    weights=[40, 25, 15, 15, 5],
                )[0]
                Activity.objects.get_or_create(
                    student=student,
                    semester=semester,
                    category=category,
                    title=title,
                    defaults={
                        "description": f"{title} - {student.user.get_full_name()} tomonidan yuborildi",
                        "score": Decimal(str(score)) if status == "approved" else Decimal("0"),
                        "status": status,
                        "verified_by": admin if status != "pending" else None,
                        "verified_at": timezone.now() - timedelta(days=random.randint(1, 30)) if status != "pending" else None,
                        "proof_url": f"https://example.com/proof/{student.student_id}/{category}",
                    },
                )

            ascore, _ = ActivityScore.objects.get_or_create(
                student=student,
                semester=semester,
            )
            ascore.recalculate()

    def _create_evaluations(self, students, semester, tutors, komendants, manager, teachers):
        self.stdout.write("  Creating evaluations...")
        for student in students:
            tutor = student.tutor or random.choice(tutors)
            TutorEvaluation.objects.get_or_create(
                student=student,
                semester=semester,
                evaluator=tutor,
                defaults={
                    "corporate_culture": Decimal(str(random.choice([0, 0.5, 0.5, 1, 1]))),
                    "social_activity": Decimal(str(random.choice([0, 0.5, 0.5, 1, 1]))),
                    "soft_skills": Decimal(str(random.choice([0, 0.5, 1, 1]))),
                    "discipline": Decimal(str(random.choice([0, 0.5, 0.5, 1, 1]))),
                    "dormitory": Decimal(str(random.choice([0, 0.5, 1, 1]))),
                    "comment": random.choice([
                        "Faol va intizomli talaba",
                        "Yaxshi natijalar ko'rsatmoqda",
                        "O'rtacha faollik",
                        "Ijtimoiy hayotda faol",
                        "Intizom masalalari bor",
                        "Rivojlanish sur'ati yaxshi",
                    ]),
                },
            )

            if random.random() < 0.6:
                komendant = random.choice(komendants)
                try:
                    TutorEvaluation.objects.get_or_create(
                        student=student,
                        semester=semester,
                        evaluator=komendant,
                        defaults={
                            "corporate_culture": Decimal(str(random.choice([0.5, 1]))),
                            "social_activity": Decimal(str(random.choice([0, 0.5, 1]))),
                            "soft_skills": Decimal(str(random.choice([0.5, 1]))),
                            "discipline": Decimal(str(random.choice([0, 0.5, 1]))),
                            "dormitory": Decimal(str(random.choice([0.5, 0.5, 1, 1]))),
                            "comment": random.choice([
                                "Yotoqxona faoliyatida faol",
                                "Tartibli va mas'uliyatli",
                                "Yotoqxona qoidalariga rioya qiladi",
                                "Universitet tadbirlarida qatnashadi",
                            ]),
                        },
                    )
                except Exception:
                    pass

            if random.random() < 0.4:
                try:
                    TutorEvaluation.objects.get_or_create(
                        student=student,
                        semester=semester,
                        evaluator=manager,
                        defaults={
                            "corporate_culture": Decimal(str(random.choice([0.5, 1]))),
                            "social_activity": Decimal(str(random.choice([0, 0.5, 1]))),
                            "soft_skills": Decimal(str(random.choice([0.5, 1]))),
                            "discipline": Decimal(str(random.choice([0.5, 1]))),
                            "dormitory": Decimal(str(random.choice([0, 0.5, 1]))),
                            "comment": random.choice([
                                "Sport mashg'ulotlarida faol",
                                "Jismoniy tarbiya bo'yicha yaxshi natijalar",
                                "Sport musobaqalarida qatnashgan",
                            ]),
                        },
                    )
                except Exception:
                    pass

            mentor = student.mentor or random.choice(teachers)
            MentorFeedback.objects.get_or_create(
                student=student,
                semester=semester,
                mentor=mentor,
                defaults={
                    "technical_skills": random.choices(
                        ["excellent", "good", "average", "below_average"],
                        weights=[20, 40, 30, 10],
                    )[0],
                    "participation": random.choices(
                        ["excellent", "good", "average", "below_average"],
                        weights=[15, 45, 30, 10],
                    )[0],
                    "teamwork": random.choices(
                        ["excellent", "good", "average", "below_average"],
                        weights=[20, 40, 30, 10],
                    )[0],
                    "initiative": random.choices(
                        ["excellent", "good", "average", "below_average", "poor"],
                        weights=[15, 35, 30, 15, 5],
                    )[0],
                    "overall_comment": random.choice([
                        f"{student.user.get_full_name()} texnik jihatdan kuchli talaba",
                        f"{student.user.get_full_name()} jamoa ishida faol qatnashadi",
                        f"{student.user.get_full_name()} mustaqil ish qobiliyati yaxshi",
                        f"{student.user.get_full_name()} rivojlanish dinamikasi ijobiy",
                        f"{student.user.get_full_name()} qo'shimcha e'tibor talab qiladi",
                    ]),
                    "recommendations": random.choice([
                        "Mustaqil loyihalarda ko'proq ishlashi kerak",
                        "Algoritmik bilimlarini kuchaytirishi lozim",
                        "Jamoa loyihalarida liderlik qilishi mumkin",
                        "Open source loyihalarga qo'shilishi tavsiya etiladi",
                        "",
                    ]),
                },
            )

            DisciplineRecord.objects.get_or_create(
                student=student,
                semester=semester,
                defaults={
                    "academic_honesty": Decimal(str(max(0, min(10, round(random.gauss(8, 1.5), 2))))),
                    "recorded_by": random.choice([*tutors, *komendants]),
                    "note": random.choice([
                        "Tartib-intizomga rioya qiladi",
                        "Yaxshi natijalar",
                        "Ba'zi intizom masalalari mavjud",
                        "Universitet qoidalariga to'liq amal qiladi",
                        "",
                    ]),
                },
            )

    def _create_penalties(self, students, semester, admin, tutors, komendants):
        self.stdout.write("  Creating penalties and recoveries...")
        penalty_data = [
            ("light", "late", -1, "Darsga kechikish"),
            ("light", "late", -1, "Mashg'ulotga kechikish"),
            ("light", "phone", -1, "Dars vaqtida telefon ishlatish"),
            ("medium", "absent", -3, "Sababsiz dars qoldirish"),
            ("medium", "dormitory", -3, "Yotoqxona qoidalari buzilishi"),
            ("medium", "ignore_warning", -3, "Ogohlantirishni e'tiborsiz qoldirish"),
            ("medium", "rule_violation", -3, "Tartib qoidalarini buzish"),
            ("heavy", "cheating", -10, "Imtihonda ko'chirish"),
            ("heavy", "systematic_absent", -8, "Tizimli dars qoldirish (5+ marta)"),
            ("heavy", "discipline_issue", -5, "Jiddiy intizom buzilishi"),
        ]

        recovery_tasks = [
            "Kutubxonada 10 soat ishlash",
            "Qo'shimcha laboratoriya ishi bajarish",
            "Talabalar uchun seminar o'tkazish",
            "Open source loyihaga hissa qo'shish",
            "Volontyor sifatida tadbir tashkil qilish",
            "Professor bilan qo'shimcha ish",
            "Texnik maqola yozish",
            "Junior talabalarga mentorlik qilish",
        ]

        all_issuers = [admin] + tutors + komendants
        for student in students:
            if random.random() < 0.3:
                continue
            num_penalties = random.choices([1, 2, 3, 4], weights=[40, 30, 20, 10])[0]
            for _ in range(num_penalties):
                sev, cat, pts, desc = random.choice(penalty_data)
                Penalty.objects.create(
                    student=student,
                    semester=semester,
                    severity=sev,
                    category=cat,
                    points=Decimal(str(pts)),
                    description=desc,
                    issued_by=random.choice(all_issuers),
                )

            if random.random() < 0.6:
                num_recoveries = random.randint(1, 2)
                for _ in range(num_recoveries):
                    rec_status = random.choices(
                        ["completed", "completed", "in_progress", "assigned", "failed"],
                        weights=[35, 25, 20, 15, 5],
                    )[0]
                    Recovery.objects.create(
                        student=student,
                        semester=semester,
                        task_description=random.choice(recovery_tasks),
                        recovery_points=Decimal(str(random.randint(1, 5))) if rec_status == "completed" else Decimal("0"),
                        status=rec_status,
                        assigned_by=random.choice(all_issuers),
                        completed_at=timezone.now() - timedelta(days=random.randint(1, 20)) if rec_status == "completed" else None,
                        review_note=random.choice([
                            "Vazifa to'liq bajarildi",
                            "Yaxshi harakat ko'rsatdi",
                            "Qoniqarli natija",
                            "",
                        ]) if rec_status == "completed" else "",
                    )

            summary, _ = PenaltySummary.objects.get_or_create(
                student=student,
                semester=semester,
            )
            summary.recalculate()

    def _create_employment(self, students, semester):
        self.stdout.write("  Creating employment records...")
        companies = [
            ("EPAM Systems", "Junior Developer", "internship", 4),
            ("Uzum", "Backend Intern", "internship", 3),
            ("Najot Ta'lim", "Part-time Mentor", "part_time", 6),
            ("Google", "SWE Intern", "internship", 5),
            ("PDP Academy", "Lab Assistant", "part_time", 5),
            ("Exadel", "QA Intern", "internship", 3),
            ("Payme", "Frontend Developer", "part_time", 7),
            ("Click", "Mobile Dev Intern", "internship", 4),
            ("Udevs", "Full-stack Developer", "full_time", 10),
            ("Zero One Group", "Junior Backend", "part_time", 6),
            ("Abutech", "DevOps Intern", "internship", 4),
            ("IT Park", "Resident Developer", "part_time", 5),
        ]

        for student in students:
            if random.random() < 0.45:
                continue
            company, position, etype, score = random.choice(companies)
            EmploymentRecord.objects.get_or_create(
                student=student,
                semester=semester,
                defaults={
                    "employment_type": etype,
                    "company_name": company,
                    "position": position,
                    "start_date": date(2025, 9, 1) + timedelta(days=random.randint(0, 90)),
                    "score": Decimal(str(score)),
                    "status": random.choices(
                        ["approved", "approved", "approved", "pending"],
                        weights=[40, 30, 20, 10],
                    )[0],
                    "proof_url": f"https://example.com/employment/{student.student_id}",
                },
            )
