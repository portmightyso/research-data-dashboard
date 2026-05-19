from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ResearchProject

# ۱. مدیریت صفحه لاگین (GET برای دیدن صفحه، POST برای بررسی یوزرنیم و پسورد)
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard_home') # اگر قبلاً لاگین کرده مستقیم برود به داشبورد
        return render(request, 'login.html')

    def post(self, request):
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        
        # استفاده از سیستم احراز هویت داخلی جنگو
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_home')
        else:
            return render(request, 'login.html', {'error': 'Invalid Username or Password!'})

# ۲. متد خروج از حساب کاربری
def logout_view(request):
    logout(request)
    return redirect('login_view')

# ۳. نمایش داشبورد اصلی (فقط اساتیدی که لاگین کرده‌اند حق ورود دارند)
@method_decorator(login_required(login_url='login_view'), name='dispatch')
class DashboardHome(View):
    def get(self, request):
        # نام استاد لاگین شده را می‌فرستیم به صفحه HTML
        return render(request, 'index.html', {'professor_name': request.user.username})

# ۴. مدیریت دیتابیس پروژه‌ها با قفل خودکار نام استاد
@method_decorator(csrf_exempt, name='dispatch')
class ProjectListAPI(View):
    def get(self, request, *args, **kwargs):
        projects = ResearchProject.objects.all()
        data = []
        for p in projects:
            data.append({
                'id': p.id,
                'title': p.title,
                'researcher': p.researcher_name,
                'date': p.created_at.strftime('%Y-%m-%d')
            })
        return JsonResponse({'projects': data}, safe=False)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)
            
        body = json.loads(request.body)
        
        # جادو اینجا اتفاق می‌افتد: نام محقق مستقیماً از کاربر لاگین شده (request.user.username) گرفته می‌شود!
        new_project = ResearchProject.objects.create(
            title=body['title'],
            researcher_name=request.user.username 
        )
        return JsonResponse({
            'status': 'success',
            'project': {
                'id': new_project.id,
                'title': new_project.title,
                'researcher': new_project.researcher_name,
                'date': new_project.created_at.strftime('%Y-%m-%d')
            }
        })

    def delete(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            project_id = body.get('id')
            project = ResearchProject.objects.get(id=project_id)
            project.delete()
            return JsonResponse({'status': 'success', 'message': 'Project deleted successfully'})
        except ResearchProject.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Project not found'}, status=404)
        # ۱. حتماً مطمئن شو که بالا فولد اِسم درست را ایمپورت کردی:
from .models import ResearchProject, ExperimentData  # <-- اصلاح شد

@method_decorator(csrf_exempt, name='dispatch')
class ExperimentLogAPI(View):
    def get(self, request, *args, **kwargs):
        # گرفتن تمام داده‌ها از مدل کدهای خودت
        logs = ExperimentData.objects.all()  # <-- اصلاح شد
        data = []
        for log in logs:
            data.append({
                'id': log.id,
                'projectId': log.project.id,
                'name': log.dataset_name,
                'value': log.measured_value,
                'notes': log.notes
            })
        return JsonResponse({'experiments': data}, safe=False)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)
            
        body = json.loads(request.body)
        
        try:
            project = ResearchProject.objects.get(id=body['projectId'])
        except ResearchProject.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Project not found'}, status=404)
            
        # ذخیره در مدل کدهای خودت
        new_log = ExperimentData.objects.create(  # <-- اصلاح شد
            project=project,
            dataset_name=body['name'],
            measured_value=float(body['value']),
            notes=body.get('notes', '')
        )
        
        return JsonResponse({
            'status': 'success',
            'experiment': {
                'id': new_log.id,
                'projectId': new_log.project.id,
                'name': new_log.dataset_name,
                'value': new_log.measured_value,
                'notes': new_log.notes
            }
        })

    def delete(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            log_id = body.get('id')
            log = ExperimentData.objects.get(id=log_id)  # <-- اصلاح شد
            log.delete()
            return JsonResponse({'status': 'success', 'message': 'Log deleted successfully'})
        except ExperimentData.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Log not found'}, status=404)