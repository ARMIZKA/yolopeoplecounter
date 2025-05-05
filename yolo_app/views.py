import os

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from ultralytics import YOLO
import cv2

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from PIL import Image, UnidentifiedImageError

from .models import Report


model = YOLO(os.path.join(settings.BASE_DIR, 'models', 'yolov8s.pt'))


FONT_NAME = "DejaVuSans"
FONT_PATH = os.path.join(settings.BASE_DIR, 'yolo_app', 'static', 'fonts', 'DejaVuSans.ttf')
pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))


def detect_people(image_path: str):
    results = model(image_path, classes=[0])
    count = len(results[0].boxes)


    annotated = results[0].plot()
    base = os.path.splitext(os.path.basename(image_path))[0]
    result_name = f"{base}_result.jpg"
    result_path = os.path.join(settings.MEDIA_ROOT, result_name)
    cv2.imwrite(result_path, annotated)

    return count, settings.MEDIA_URL + result_name


def generate_pdf(count: int, image_path: str, pdf_path: str):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    c.setFont(FONT_NAME, 16)
    c.drawString(72, height - 72, "Отчёт")
    c.setFont(FONT_NAME, 14)
    c.drawString(72, height - 100, f"Найдено посетителей: {count}")

    img = ImageReader(image_path)
    img_w, img_h = img.getSize()
    max_w = width - 2 * 72
    scale = max_w / img_w
    draw_w = max_w
    draw_h = img_h * scale
    c.drawImage(img, 72, height - 100 - draw_h - 20, width=draw_w, height=draw_h)

    c.showPage()
    c.save()


def index(request):
    context = {}

    if request.method == 'POST' and request.FILES.get('image'):
        uploaded = request.FILES['image']

        try:
            img = Image.open(uploaded)
            img.verify()
        except (UnidentifiedImageError, OSError):
            context['error'] = "Загруженный файл не является изображением. Пожалуйста, выберите корректный файл."
            return render(request, 'yolo_app/index.html', context)

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(uploaded.name, uploaded)
        full_image_path = fs.path(filename)


        count, result_url = detect_people(full_image_path)


        result_name = os.path.basename(result_url)
        result_path = os.path.join(settings.MEDIA_ROOT, result_name)
        base = os.path.splitext(result_name)[0]
        pdf_name = f"{base}_report.pdf"
        pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_name)
        generate_pdf(count, result_path, pdf_path)
        pdf_url = settings.MEDIA_URL + pdf_name

        Report.objects.create(
            original_image=filename,
            result_image=result_name,
            pdf_report=pdf_name,
            count=count
        )

        context.update({
            'count': count,
            'result_url': result_url,
            'pdf_url': pdf_url,
        })


    history = Report.objects.all()[:10]
    context['history'] = history

    return render(request, 'yolo_app/index.html', context)
