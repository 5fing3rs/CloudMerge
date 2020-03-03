from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .models import *
from .forms import *

from .Code.test import IOI


def index(request):
    latest_input_image_list = Input_Image.objects.order_by('-input_upload_time')[:]
    context = {'latest_input_image_list': latest_input_image_list}
    return render(request, 'ioi/index.html', context)


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
