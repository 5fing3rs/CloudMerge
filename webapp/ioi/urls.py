from django.urls import path

from . import views

app_name = 'ioi'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('<int:input_image_id>/', views.detail, name='detail'),
]
