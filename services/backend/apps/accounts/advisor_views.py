from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from django.conf import settings
from .models import User, StudentProfile
from apps.grants.models import GrantScore
from apps.attendance.models import AttendanceSummary
from apps.assignments.models import AssignmentScore
from apps.penalties.models import PenaltySummary
import openai
import environ

env = environ.Env()

class AdvisorChatView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        message = request.data.get("message", "")
        student_id_param = request.data.get("student_id")

        if not message:
            return Response({"error": "Xabar (message) yuborilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Determine which student profile to use
        student_profile = None
        if user.role == User.Role.STUDENT:
            try:
                student_profile = user.student_profile
            except StudentProfile.DoesNotExist:
                raise NotFound("Talaba profili topilmadi.")
        elif user.role == User.Role.PARENT:
            if not student_id_param:
                # If no student_id provided, default to first child
                student_profile = StudentProfile.objects.filter(parent=user).first()
                if not student_profile:
                    raise NotFound("Sizga biriktirilgan farzand topilmadi.")
            else:
                student_profile = StudentProfile.objects.filter(parent=user, student_id=student_id_param).first()
                if not student_profile:
                    raise PermissionDenied("Siz bu talaba ma'lumotlariga ruxsatga ega emassiz.")
        else:
            raise PermissionDenied("Faqat talaba va ota-onalar ushbu xizmatdan foydalanishi mumkin.")

        # 2. Gather Academic Context
        context_data = self.gather_student_context(student_profile)

        # 3. Call OpenAI API
        openai_api_key = env("OPENAI_API_KEY", default="")
        if not openai_api_key:
             return Response({"error": "AI xizmati hozircha faol emas (API Kalit o'rnatilmagan)."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        client = openai.OpenAI(api_key=openai_api_key)

        system_prompt = f"""
Siz PDP Universiteti "EduMetric CRM" tizimining "Sun'iy Intellekt Akademik Maslahatchisi" (AI Academic Advisor) hisoblanasiz.
Foydalanuvchi talaba ({student_profile.user.get_full_name()}) yoki uning ota-onasi bo'lishi mumkin. Siz ularga talabaning akademik holati, davomati, topshiriqlari, jarimalari va granti haqidagi ma'lumotlarni tushuntirib, grantini saqlab qolish yoki reytingini oshirish bo'yicha maslahatlar berishingiz kerak.

TALABA HAQIDAGI MA'LUMOTLAR:
{context_data}

VAZIFALARINGIZ:
1. Foydalanuvchining so'rovlariga ushbu ma'lumotlardan kelib chiqib aniq, xushmuomala va yordamga tayyor ruhda o'zbek tilida javob bering.
2. Agar talabaning granti xavf ostida bo'lsa (masalan davomati past, GPA 80% dan tushib ketgan yoki jarimalari bo'lsa), buni aniq ko'rsating va tiklash uchun (masalan 'recovery task' yoki qo'shimcha ballar olish) nima qilish kerakligini maslahat bering.
3. Yo'q ma'lumotlarni to'qimang. Faqatgina berilgan raqamlar asosida xulosa qiling.
4. Javoblaringizni Markdown formatida, paragraf va ro'yxatlar bilan chiroyli shaklda bering. Xabar oxirida omad tilab, o'z yordamingizni taklif qilishni unutmang.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=800
            )
            ai_reply = response.choices[0].message.content
            return Response({"reply": ai_reply})
        except Exception as e:
            return Response({"error": f"AI bilan bog'lanishda xatolik yuz berdi: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def gather_student_context(self, profile):
        parts = []
        parts.append(f"Ism-sharif: {profile.user.get_full_name()}")
        parts.append(f"Guruh: {profile.group}, Kurs: {profile.course}, Holat: {profile.get_status_display()}, Grant Holati: {profile.get_grant_status_display()}")
        
        # Grant Score
        grant_score = GrantScore.objects.filter(student=profile).order_by('-semester__id').first()
        if grant_score:
            parts.append(f"--- JORIY REYTING (Semestr: {grant_score.semester.name}) ---")
            parts.append(f"Asosiy Ball: {grant_score.base_total}/100, Yakuniy Ball: {grant_score.final_score}")
            parts.append(f"Rank (O'rni): {grant_score.rank if grant_score.rank else 'Hali belgilanmagan'}")
            parts.append(f"GPA: {grant_score.gpa_percentage}% (Grant uchun >80% talab etiladi. Status: {'Bajarilgan' if grant_score.gpa_eligible else 'Bajarilmagan'})")
            parts.append(f"Tarkibiy ballar: Akademik: {grant_score.academic_score}/40, Davomat: {grant_score.attendance_score}/20, Topshiriqlar: {grant_score.assignment_score}/15, Faollik: {grant_score.activity_score}/10, Tyutor: {grant_score.tutor_score}/5, Intizom: {grant_score.discipline_score}/10")
            parts.append(f"Jarimalar: {grant_score.penalty_score}, Tiklanish (Recovery): +{grant_score.recovery_score}, Bandlik Bonusi: +{grant_score.employment_score}")
        
        # Attendance Summary
        att_summary = AttendanceSummary.objects.filter(student=profile).order_by('-semester__id').first()
        if att_summary:
            parts.append(f"--- DAVOMAT ---")
            parts.append(f"Jami darslar: {att_summary.total_classes}, Qatnashgan: {att_summary.attended_classes}, Foiz: {att_summary.percentage}%")

        # Assignment Summary
        asn_summary = AssignmentScore.objects.filter(student=profile).order_by('-semester__id').first()
        if asn_summary:
            parts.append(f"--- TOPSHIRIQLAR ---")
            parts.append(f"Jami topshiriqlar: {asn_summary.total_assignments}, Bajarilgan: {asn_summary.completed_assignments}, O'rtacha sifat (100 dan): {asn_summary.average_quality_score}")
            
        # Penalty Summary
        pen_summary = PenaltySummary.objects.filter(student=profile).order_by('-semester__id').first()
        if pen_summary and pen_summary.net_penalty < 0:
            parts.append(f"--- JAZOLAR VA TIKLANISH ---")
            parts.append(f"Jami jarima: {pen_summary.total_penalty}, Qoplangan (Recovery): {pen_summary.total_recovery}, Umumiy: {pen_summary.net_penalty}")

        return "\n".join(parts)
