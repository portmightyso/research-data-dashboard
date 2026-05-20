from django.db import models

class ResearchProject(models.Model):
    title = models.CharField(max_length=255)
    researcher_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ExperimentData(models.Model):
    # تعریف گزینه‌های وضعیت برای دیتابیس
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('anomaly', 'Noise / Anomaly'),
        ('retest', 'Needs Retest'),
    ]

    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, related_name='experiments')
    dataset_name = models.CharField(max_length=255)
    measured_value = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='success') # فیلد جدید
    lab_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.dataset_name