from django import forms


class UploadImageForm(forms.Form):
    input_calib_url = forms.CharField(label='Input calib URL', max_length=255)
    input_image_2_url = forms.CharField(label='Input image_2 URL', max_length=255)
    input_label_2_url = forms.CharField(label='Input label_2 URL', max_length=255)
    input_velodyne_url = forms.CharField(label='Input velodyne URL', max_length=255)


class ProcessImageForm(forms.Form):
    output_folder_url = forms.CharField(label='Output folder URL', max_length=255)

class UploadCloudForm(forms.Form):
    input_cloud_url = forms.CharField(label='Input image cloud URL', max_length=255)

class ProcessCloudForm(forms.Form):
    output_folder_url = forms.CharField(label='Output folder URL', max_length=255)
