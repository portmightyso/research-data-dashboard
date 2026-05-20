import json
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ResearchProject, ExperimentData

# ۱. کلاس نمایش صفحه اصلی داشبورد (که رندر به خاطرش ارور می‌داد)
class DashboardHome(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = '/login/'  # اگر کاربر لاگین نبود، هدایت می‌شود به صفحه لاگین

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # فرستادن نام استاد به قالب HTML
        context['professor_name'] = self.request.user.username if self.request.user.is_authenticated else "Soroush"
        return context

# ۲. مدیریت API مربوط به پروژه‌ها
@method_decorator(csrf_exempt, name='dispatch')
class ProjectAPI(View):
    def get(self, request, *args, **kwargs):
        projects = ResearchProject.objects.all()
        data = []
        for p in projects:
            data.append({
                'id': p.id,
                'title': p.title,
                'researcher': p.researcher_name,
                'date': p.created_at.strftime('%Y-%m-%d') if p.created_at else ''
            })
        return JsonResponse({'projects': data}, safe=False)

def post(self, request, *args, **kwargs):
        # بررسی اینکه آیا کاربر واقعاً لاگین است یا خیر
        if request.user.is_authenticated:
            researcher = request.user.username
        else:
            researcher = "Prof. Soroush"

        try:
            body = json.loads(request.body)
            # ایجاد و ذخیره مستقیم در دیتابیس نئون
            new_project = ResearchProject.objects.create(
                title=body['title'],
                researcher_name=researcher
            )
            return JsonResponse({
                'status': 'success',
                'project': {
                    'id': new_project.id,
                    'title': new_project.title,
                    'researcher': new_project.researcher_name,
                    'date': new_project.created_at.strftime('%Y-%m-%d') if new_project.created_at else ''
                }
            })
        except Exception as e:
            # این خط باعث می‌شود اگر نئون اروری داد (مثل نبودن جدول یا فیلد اضافه)، توی کنسول مرورگر متوجه بشوی
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            project_id = body.get('id')
            project = ResearchProject.objects.get(id=project_id)
            project.delete()
            return JsonResponse({'status': 'success', 'message': 'Project deleted successfully'})
        except ResearchProject.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Project not found'}, status=404)

# ۳. مدیریت API مربوط به لاگ‌های آزمایشگاهی (ExperimentLogAPI)
@method_decorator(csrf_exempt, name='dispatch')
class ExperimentLogAPI(View):
    def get(self, request, *args, **kwargs):
        experiments = ExperimentData.objects.all()
        data = []
        for e in experiments:
            data.append({
                'id': e.id,
                'projectId': e.project.id if e.project else None,
                'name': e.dataset_name,
                'value': float(e.measured_value) if e.measured_value else 0.0,
                'notes': e.lab_notes
            })
        return JsonResponse({'experiments': data}, safe=False)

    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            project = ResearchProject.objects.get(id=body['projectId'])
            
            new_log = ExperimentData.objects.create(
                project=project,
                dataset_name=body['name'],
                measured_value=body['value'],
                lab_notes=body.get('notes', '')
            )
            return JsonResponse({
                'status': 'success',
                'experiment': {
                    'id': new_log.id,
                    'projectId': project.id,
                    'name': new_log.dataset_name,
                    'value': float(new_log.measured_value),
                    'notes': new_log.lab_notes
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            log_id = body.get('id')
            log = ExperimentData.objects.get(id=log_id)
            log.delete()
            return JsonResponse({'status': 'success', 'message': 'Log deleted successfully'})
        except ExperimentData.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Log not found'}, status=404)