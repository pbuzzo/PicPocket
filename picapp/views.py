from django.shortcuts import render
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
from django.views.generic import View
from subprocess import check_output
from picapp.forms import ImageForm
import exifread as ef
import re





class ScanImage(View):
    def get(self, request):
        html = "index.html"
        # img = Image.open("picapp/static/img/testppc.jpg")
        # img_exif = img.getexif()
        # new_dict = []
        # if img_exif:
        #     img_exif_dict = dict(img_exif)
        #     for key, val in img_exif_dict.items():
        #         if key in ExifTags.TAGS:
        #             new_dict.append(str(ExifTags.TAGS[key]) + " - " + str(val))
        # else:
        #     new_dict.append('No Exif Data, sorry!')
        return render(request, html)


    def post(self, request):
        """Process images uploaded by users"""
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                # Get the current instance object to display in the template
                img_obj = form.instance
                img = Image.open(img_obj.image)
                img_exif = img._getexif()
                new_dict = []
                coords = []
                if img_exif:
                    img_exif_dict = dict(img_exif)
                    for key, val in img_exif_dict.items():
                        if key in ExifTags.TAGS:
                            new_dict.append(str(ExifTags.TAGS[key]) + " - " + str(val))
                else:
                    new_dict.append('No Exif Data, sorry!')
                tags = ef.process_file(img_obj.image)
                for item in new_dict:
                    GPS_find = re.findall('GPSInfo', item)
                    for i in GPS_find:
                        coords.append(item)
                        new_dict.remove(item)
                return render(request, 'index.html', {'form': form, 'img_obj': img_obj, 'photo': new_dict, 'coords': coords})
        else:
            form = ImageForm()
        return render(request, 'index.html', {'form': form})
