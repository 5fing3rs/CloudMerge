from django.db import models


class Input_Image(models.Model):
    input_id = models.IntegerField(primary_key=True)
    input_calib_url = models.CharField(max_length=255)
    input_image_2_url = models.CharField(max_length=255)
    input_label_2_url = models.CharField(max_length=255)
    input_velodyne_url = models.CharField(max_length=255)
    input_upload_time = models.DateTimeField('Upload time')

    def __str__(self):
        return str(self.input_id)


class Output_Image(models.Model):
    input_id = models.ForeignKey(Input_Image, on_delete=models.PROTECT)
    output_folder_url = models.CharField(max_length=255)

    def __str__(self):
        return self.output_folder_url

class Input_cloud(models.Model):
    input_id = models.IntegerField(primary_key=True)
    # input_calib_url = models.CharField(max_length=255)
    input_cloud_2_url = models.CharField(max_length=255)
    # input_label_2_url = models.CharField(max_length=255)
    # input_velodyne_url = models.CharField(max_length=255)
    input_upload_time = models.DateTimeField('Upload time')

    def __str__(self):
        return str(self.input_id)

class Output_cloud(models.Model):
    input_id = models.ForeignKey(Input_cloud, on_delete=models.PROTECT)
    output_folder_url = models.CharField(max_length=255)

    def __str__(self):
        return output_folder_url