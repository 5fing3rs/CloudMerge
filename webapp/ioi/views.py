from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .models import *
from .forms import *

from .Code.test import *
# from .Code.test import ND

def index(request):
    latest_input_image_list = Input_Image.objects.order_by('-input_upload_time')[:]
    context = {'latest_input_image_list': latest_input_image_list}
    return render(request, 'ioi/index.html', context)

def noise_index(request):
    latest_input_cloud_list = Input_cloud.objects.order_by('-input_upload_time')[:]
    context = {'latest_input_cloud_list': latest_input_cloud_list}
    return render(request,'ioi/noise_index.html', context)

def object_index(request):
    latest_input_cloud_list = Input_cloud.objects.order_by('-input_upload_time')[:]
    context = {'latest_input_cloud_list': latest_input_cloud_list}
    return render(request,'ioi/object_index.html', context)

def seperation_index(request):
    latest_input_cloud_list = Input_cloud.objects.order_by('-input_upload_time')[:]
    context = {'latest_input_cloud_list': latest_input_cloud_list}
    return render(request,'ioi/seperation_index.html', context)


def welcome(request):
    return render(request, 'ioi/welcome.html')

def upload_image(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST)
        if form.is_valid():
            input_image = Input_Image(input_calib_url=form.cleaned_data["input_calib_url"],
                                      input_image_2_url=form.cleaned_data["input_image_2_url"],
                                      input_label_2_url=form.cleaned_data["input_label_2_url"],
                                      input_velodyne_url=form.cleaned_data["input_velodyne_url"],
                                      input_upload_time=timezone.now())
            input_image.save()
            return HttpResponseRedirect('/ioi/upload_image')
    else:
        form = UploadImageForm()
    return render(request, 'ioi/upload_image.html', {'form': form})

def upload_cloud(request):
    if request.method == 'POST':
        form = UploadCloudForm(request.POST)
        if form.is_valid():
            input_cloud = Input_cloud(input_cloud_2_url=form.cleaned_data["input_cloud_url"],
                                        input_upload_time=timezone.now())
            input_cloud.save()
            return HttpResponseRedirect('/ioi/upload_cloud')
    else:
        form = UploadCloudForm()
    return render(request, 'ioi/upload_cloud.html', {'form': form})


def detail(request, input_image_id):
    input_image = get_object_or_404(Input_Image, pk=input_image_id)
    if request.method == "POST":
        form = ProcessImageForm(request.POST)
        if form.is_valid():
            output_image = Output_Image(input_id=input_image,
                                        output_folder_url=form.cleaned_data["output_folder_url"])
            output_image.save()
            IOI(input_image.input_calib_url,
                input_image.input_image_2_url,
                input_image.input_label_2_url,
                input_image.input_velodyne_url,
                form.cleaned_data["output_folder_url"])
            context = {'input_image': input_image,
                       'process': True,
                       'output_folder_url': form.cleaned_data["output_folder_url"],
                       'form': form}
    else:
        form = ProcessImageForm()
        context = {'input_image': input_image,
                   'process': False,
                   'form': form}
    return render(request, 'ioi/detail.html', context)

def noise_detail(request, input_cloud_id):
    # empty_form = DocumentForm(request.POST,request.FILES)
    input_cloud = get_object_or_404(Input_cloud, pk=input_cloud_id)
    if request.method == "POST":
        form = ProcessCloudForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data["output_folder_url"])
            # output_cloud = Output_cloud(input_id=input_cloud,
                                        # output_folder_url=form.cleaned_data["output_folder_url"])
            # output_cloud.save()
            ND(input_cloud.input_cloud_2_url,
                form.cleaned_data["output_folder_url"])
            context = {'input_cloud': input_cloud,
                       'process': True,
                       'output_folder_url': form.cleaned_data["output_folder_url"],
                       'form': form}
            
    else:
        form = ProcessCloudForm()
        context = {'input_cloud': input_cloud,
                   'process': False,
                   'form': form}
    return render(request, 'ioi/noise_detail.html', context)

def object_detail(request, input_cloud_id):
    input_cloud = get_object_or_404(Input_cloud, pk=input_cloud_id)
    if request.method == "POST":
        form = ProcessCloudForm(request.POST)
        if form.is_valid():
            # output_cloud = Output_cloud(input_id=input_cloud,
                                        # output_folder_url=form.cleaned_data["output_folder_url"])
            # output_cloud.save()
            OD(input_cloud.input_cloud_2_url,
                form.cleaned_data["output_folder_url"])
            context = {'input_cloud': input_cloud,
                       'process': True,
                       'output_folder_url': form.cleaned_data["output_folder_url"],
                       'form': form}
    else:
        form = ProcessCloudForm()
        context = {'input_cloud': input_cloud,
                   'process': False,
                   'form': form}
    return render(request, 'ioi/object_detail.html', context)

def seperation_detail(request, input_cloud_id):
    input_cloud = get_object_or_404(Input_cloud, pk=input_cloud_id)
    if request.method == "POST":
        form = ProcessCloudForm(request.POST)
        if form.is_valid():
            # output_cloud = Output_cloud(input_id=input_cloud,
                                        # output_folder_url=form.cleaned_data["output_folder_url"])
            # output_cloud.save()
            SD(input_cloud.input_cloud_2_url,
                form.cleaned_data["output_folder_url"])
            context = {'input_cloud': input_cloud,
                       'process': True,
                       'output_folder_url': form.cleaned_data["output_folder_url"],
                       'form': form}
    else:
        form = ProcessCloudForm()
        context = {'input_cloud': input_cloud,
                   'process': False,
                   'form': form}
    return render(request, 'ioi/seperation_detail.html', context)

