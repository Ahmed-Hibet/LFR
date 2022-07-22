from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from license.forms import LicenseRequirement
import requests


class Home(View):
    def get(self, request):
        url = "http://127.0.0.1:2000/api/services/facility/pending/"
        pending_facility_objects =requests.get(url)
        if pending_facility_objects.status_code != 200:
            return HttpResponse(status=pending_facility_objects.status_code)
        pending_facility_list = pending_facility_objects.json()
        return render(request, 'license/home.html', {'pending_facility_list': pending_facility_list})

class LicenseRequest(View):
    def get(self, request, pk):
        form = LicenseRequirement()
        url = "http://127.0.0.1:2000/api/services/facility/license-request/" + str(pk) + "/"
        facility_object = requests.get(url)
        if facility_object.status_code == 200:
            facility = facility_object.json()
        else:
            return HttpResponse(status=facility_object.status_code)
        return render(request, 'license/license-request.html', {'form': form, 'facility': facility})

    def post(self, request, pk):
        url = "http://127.0.0.1:2000/api/services/facility/license-request/" + str(pk) + "/"
        facility_object = requests.get(url)
        if facility_object.status_code == 200:
            facility = facility_object.json()
        else:
            return HttpResponse(status=facility_object.status_code)
        
        form = LicenseRequirement(request.POST)

        if form.is_valid():
            new_facility = {}
            new_facility['id'] = pk
            new_facility['number_of_medical_doctor'] = form.cleaned_data['number_of_medical_doctor']
            new_facility['number_of_nurse'] = form.cleaned_data['number_of_nurse']
            new_facility['number_of_midwife'] = form.cleaned_data['number_of_midwife']
            new_facility['facility_types'] = facility['facility_types']
            new_facility['name'] = facility['name']

            url = "http://127.0.0.1:2000/api/services/facility/license-request/" + str(pk) + "/"
            facility_object = requests.put(url, data=new_facility)
            return HttpResponseRedirect(reverse('home'))
        
        return render(request, 'license/license-request.html', {'form': form, 'facility': facility})
