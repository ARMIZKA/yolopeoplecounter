from django.db import models

class Report(models.Model):
    created_at     = models.DateTimeField(auto_now_add=True)
    original_image = models.CharField("Исходное фото", max_length=255)
    result_image   = models.CharField("Аннотированное фото", max_length=255)
    pdf_report     = models.CharField("PDF-отчёт",        max_length=255)
    count          = models.PositiveIntegerField("Кол-во посетителей")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Отчёт"
        verbose_name_plural = "Отчёты"

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} — {self.count} чел."
