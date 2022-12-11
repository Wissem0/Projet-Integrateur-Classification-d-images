from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
 
app_name = 'classimage'
urlpatterns = [
    path('', views.classimage_view, name='image_upload'),
    path('success/', views.success, name='success'),
    path('face_images/', views.display_face_images, name = 'face_images'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)