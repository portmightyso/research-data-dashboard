import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import ResearchProject, ExperimentData

# ==================== ۱. مدیریت احراز هویت و صفحات ====================

@login_required
def dashboard_view(request):
    """رندر کردن صفحه اصلی داشبورد تحقیقاتی"""
    # ارسال نام استاد/پژوهشگر به فرانت‌آند برای شخصی‌سازی محیط
    context = {
        'professor_name': request.user.username.capitalize()
    }
    return render(request, 'index.html', context)

def register_view(request):
    """ثبت‌نام پژوهشگر جدید"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard_view')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    """ورود اعضای دپارتمان به سیستم مدیریت داده"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard_view')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """خروج امن از سیستم"""
    if request.method == 'POST':
        logout(request)
        return redirect('login_view')
    return redirect('login_view')


# ==================== ۲. ماژول مدیریت پروژه‌ها (API) ====================

@csrf_exempt
@login_required
def project_api(request):
    """خط ارتباطی (API) فرانت‌آند برای افزودن، خواندن و حذف پروژه‌ها"""
    
    # دریافت لیست تمام پروژه‌های فعال
    if request.method == 'GET':
        projects = ResearchProject.objects.all().order_by('-id')
        project_list = [{
            'id': p.id,
            'title': p.title,
            'researcher': p.researcher_name
        } for p in projects]
        return JsonResponse({'projects': project_list})

    # ثبت یک پروژه تحقیقاتی جدید
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title', '').strip()
            if not title:
                return JsonResponse({'status': 'error', 'message': 'Project title is required'}, status=400)
            
            new_project = ResearchProject.objects.create(
                title=title,
                researcher_name=request.user.username
            )
            return JsonResponse({
                'status': 'success',
                'project': {
                    'id': new_project.id,
                    'title': new_project.title,
                    'researcher': new_project.researcher_name
                }
            })
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

    # حذف پروژه و تمام داده‌های متصل به آن (Cascade)
    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            project_id = data.get('id')
            ResearchProject.objects.filter(id=project_id).delete()
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)


# ==================== ۳. ماژول مدیریت داده‌های آزمایشگاهی (API) ====================

@csrf_exempt
@login_required
def experiment_log_api(request):
    """خط ارتباطی (API) فرانت‌آند برای ثبت لاگ‌ها، دریافت و حذف داده‌های فیلتر شده"""

    # دریافت تمامی لاگ‌های ثبت شده در سیستم همراه با برچسب وضعیت
    if request.method == 'GET':
        experiments = ExperimentData.objects.all().order_by('id')
        experiments_list = [{
            'id': e.id,
            'projectId': e.project.id,
            'name': e.dataset_name,
            'value': e.measured_value,
            'status': e.status,  # وضعیت کیفیت داده (Success/Anomaly/Retest)
            'notes': e.lab_notes or ''
        } for e in experiments]
        return JsonResponse({'experiments': experiments_list})

    # ثبت امن داده‌های ورودی از سنسور یا فرانت‌آند داشبورد
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            project_id = data.get('projectId')
            name = data.get('name', '').strip()
            value = data.get('value')
            status = data.get('status', 'success')
            notes = data.get('notes', '').strip()

            if not project_id or not name or value is None:
                return JsonResponse({'status': 'error', 'message': 'Missing fields'}, status=400)

            # متصل کردن لاگ به پروژه هدف از طریق کلید خارجی
            project = ResearchProject.objects.get(id=project_id)
            
            new_log = ExperimentData.objects.create(
                project=project,
                dataset_name=name,
                measured_value=float(value),
                status=status,
                lab_notes=notes
            )
            
            return JsonResponse({
                'status': 'success',
                'experiment': {
                    'id': new_log.id,
                    'projectId': new_log.project.id,
                    'name': new_log.dataset_name,
                    'value': new_log.measured_value,
                    'status': new_log.status,
                    'notes': new_log.lab_notes
                }
            })
        except ResearchProject.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Target project not found'}, status=404)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'status': 'error', 'message': 'Invalid payload format'}, status=400)

    # حذف یک لاگ آزمایشگاهی خاص
    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            log_id = data.get('id')
            ExperimentData.objects.filter(id=log_id).delete()
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)