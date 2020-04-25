from django.urls import path

from . import views

app_name = 'ioi'
urlpatterns = [
    path('ioi/', views.index, name='index'),
    path('noise_index/', views.noise_index, name='noise_index'),
    path('object_index/', views.object_index, name='object_index'),
    path('seperation_index/', views.seperation_index, name='seperation_index'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('upload_cloud',views.upload_cloud, name='upload_cloud'),
    path('', views.welcome, name='welcome'),
    path('<int:input_image_id>/', views.detail, name='detail'),
    path('<int:input_cloud_id>/noise', views.noise_detail, name='noise_detail'),
    path('<int:input_cloud_id>/object', views.object_detail, name='object_detail'),
    path('<int:input_cloud_id>/seperation', views.seperation_detail, name='seperation_detail')
]
