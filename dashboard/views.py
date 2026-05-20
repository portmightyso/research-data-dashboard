import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import ResearchProject, ExperimentData

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
        if request.user.is_authenticated:
            researcher = request.user.username
        else:
            researcher = "Prof. Soroush"

        try:
            body = json.loads(request.body)
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