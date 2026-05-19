from django.db import models

class ResearchProject(models.Model):
    # عنوان پروژه پژوهشی
    title = models.CharField(max_length=200)
    # نام محقق یا استاد مربوطه
    researcher_name = models.CharField(max_length=100)
    # تاریخ ثبت آزمایش
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class ExperimentData(models.Model):
    # اتصال داده‌ها به پروژه مربوطه (رابطه کلید خارجی)
    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, related_name='datasets')
    # نام یا شناسه این بخش از داده (مثلاً تست شماره ۱)
    dataset_name = models.CharField(max_length=150)
    # مقدار عددی ثبت شده (مثلاً ولتاژ یا خروجی کنترلر)
    measured_value = models.FloatField()
    # یادداشت‌های آزمایشگاهی
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.dataset_name} - {self.measured_value}"