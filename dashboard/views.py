from typing import Any, Dict
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.core import serializers
from datetime import datetime

import json

from .models import GeneralInfo, PerformanceMetrics, AdvancedInfo, StatusInfo, CpuHistory, MemoryHistory

from django.http import JsonResponse

def get_field_names(model):
    """Gets the field names of a Django model.

    Args:
        model: The Django model.

    Returns:
        A list of the field names.
    """
    return [field.name for field in model._meta.fields]

def switch_detail(request, dev_id):

    information = {}
    headers = []
    cpu_history = []
    mem_history = []

    try:
        cpu_history_objects = CpuHistory.objects.filter(dev_id=dev_id).order_by('-dev_date', '-dev_time')[:10]

        dev_time = [cpu_history_object.dev_time.strftime(r"%H:%M:%S") for cpu_history_object in cpu_history_objects]
        dev_date = [cpu_history_object.dev_date.isoformat() for cpu_history_object in cpu_history_objects]
        dev_cpu = [cpu_history_object.cpu_percentage_used for cpu_history_object in cpu_history_objects]

        # Combine the data into a list of objects
        data = [{'dev_time': o1, 'dev_date': o2, 'dev_cpu': o3} for o1, o2, o3 in zip(dev_time,dev_date,dev_cpu)]

        # Prepare the data for d3.js
        data_json = json.dumps(data)

        cpu_history.append(data_json)

    except Exception as e:
        print("Error creating CPU chart:\n " + str(e))

    try:
        mem_history_objects = MemoryHistory.objects.filter(dev_id=dev_id).order_by('-dev_date', '-dev_time')[:10]

        dev_time = [mem_history_object.dev_time.strftime(r"%H:%M:%S") for mem_history_object in mem_history_objects]
        dev_date = [mem_history_object.dev_date.isoformat() for mem_history_object in mem_history_objects]
        dev_mem = [mem_history_object.memory_percentage_used for mem_history_object in mem_history_objects]

        # Combine the data into a list of objects
        data = [{'dev_time': o1, 'dev_date': o2, 'dev_mem': o3} for o1, o2, o3 in zip(dev_time,dev_date,dev_mem)]

        # Prepare the data for d3.js
        data_json = json.dumps(data)

        mem_history.append(data_json)

    except Exception as e:
        print("Error creating MEM chart:\n " + str(e))

    try:
        switch = GeneralInfo.objects.get(dev_id=dev_id)
        information['dev_name'] = switch.dev_name
        information['id'] = switch.dev_id
        headers.append('dev_name')
    except:
        information['404'] = "Switch not found!"
        print(f'Switch with id [{dev_id}] not found!')

    try:
        performance_metrics_object = PerformanceMetrics.objects.get(dev_id=dev_id)
        for field in get_field_names(PerformanceMetrics):
            if field != 'id' and field != 'dev_id':
                information[f'{field}'] = performance_metrics_object.__getattribute__(field)
                headers.append(field)
    except:
        print("Device contains no Performance Metrics data")
    try:    
        advanced_info_object = AdvancedInfo.objects.get(dev_id=dev_id)
        for field in get_field_names(AdvancedInfo):
            if field != 'id' and field != 'dev_id':
                information[f'{field}'] = advanced_info_object.__getattribute__(field)
                headers.append(field)
    except:
        print("Device contains no Advanced Info data")
    try:
        status_info_object = StatusInfo.objects.get(dev_id=dev_id)
        for field in get_field_names(StatusInfo):
            if field != 'id' and field != 'dev_id':
                information[f'{field}'] = status_info_object.__getattribute__(field)
                headers.append(field)
    except:
        print("Device contains no Status Info data")

    context = {
        'information': information,
        'headers': headers,
        'cpu_history': cpu_history,
        'mem_history': mem_history,
    }
    return render(request, 'dashboard/detail.html', context)

def check_dev_status(request):
    # Perform any necessary logic to retrieve the updated dev_status values for each row
    updated_dev_status_list = {}

    # Get the row_id from the request parameters
    row_id = request.GET.get('row_id')

    # Get all of the status info objects
    status_info_objects = StatusInfo.objects.all()
    performance_metrics_objects = PerformanceMetrics.objects.all()

    # Iterate over the status info objects and add them to the list
    for status_info_object in status_info_objects:
        # Check if the dev_id matches the row_id
        if str(status_info_object.dev_id.dev_id) == f"{row_id}":
            # Create a dictionary for the row and add dev_id and dev_status
                updated_dev_status_list.update({f'{row_id}' : {'id': status_info_object.dev_id.dev_id}})
                updated_dev_status_list[f'{row_id}'].update({'dev_status': status_info_object.dev_status})
            
        

    # Iterate over the status info objects and add them to the list
    for performance_metrics_object in performance_metrics_objects:
        # Check if the dev_id matches the row_id
        if str(performance_metrics_object.dev_id.dev_id) == f"{row_id}":
            # Create a dictionary for the row and add dev_id and dev_status
            
            updated_dev_status_list[f'{row_id}'].update({'dev_cpu': performance_metrics_object.cpu_percentage_used })
            updated_dev_status_list[f'{row_id}'].update({'dev_mem': performance_metrics_object.memory_percentage_used })
            updated_dev_status_list[f'{row_id}'].update({'dev_hd': performance_metrics_object.harddisk_percentage_used })
            
    return JsonResponse(updated_dev_status_list, safe=False)


def get_all_info():
    """Returns all of the information in the model."""

    # Get all of the general info objects.
    general_info_objects = GeneralInfo.objects.all()

    # Get all of the performance metrics objects.
    performance_metrics_objects = PerformanceMetrics.objects.all()

    # Get all of the advanced info objects.
    advanced_info_objects = AdvancedInfo.objects.all()

    # Get all of the advanced info objects.
    status_info_objects = StatusInfo.objects.all()

    # Create a dictionary to store the information.
    information = {}

    # Iterate over the general info objects and add them to the dictionary.
    for general_info_object in general_info_objects:
        information[general_info_object.dev_id] = {
            'dev_name': general_info_object.dev_name,
        }

    # Iterate over the performance metrics objects and add them to the dictionary.
    performance_metrics_fields = get_field_names(PerformanceMetrics)
    for performance_metrics_object in performance_metrics_objects:
        for field in performance_metrics_fields:
            information[performance_metrics_object.dev_id.dev_id][f'{field}'] = performance_metrics_object.__getattribute__(field)

    # Iterate over the advanced info objects and add them to the dictionary.
    advanced_info_fields = get_field_names(AdvancedInfo)
    for advanced_info_object in advanced_info_objects:
        for field in advanced_info_fields:
            information[advanced_info_object.dev_id.dev_id][f'{field}'] = advanced_info_object.__getattribute__(field)

    # Iterate over the status info objects and add them to the dictionary.
    status_info_fields = get_field_names(StatusInfo)
    for status_info_object in status_info_objects:
        for field in status_info_fields:
            information[status_info_object.dev_id.dev_id][f'{field}'] = status_info_object.__getattribute__(field)
       
    # Return the information as a JSON object.
    return information

class index(generic.ListView):
    template_name = "dashboard/index.html"
    model = GeneralInfo
    context_object_name = "device_list"
    paginate_by = 150


    def get_queryset(self):
        """
        Return the first 10 rows of the observation table
        """
        return GeneralInfo.objects.all()[:10]
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        data_set_1 = []
        data_set_2 = []

        data_set_1 = PerformanceMetrics.objects.all()[:10]
        data_set_2 = AdvancedInfo.objects.all()[:10]

        context['data_set_1'] = data_set_1
        context['data_set_2'] = data_set_2

        context['information'] = get_all_info()

        print("Here is the data_set_1" + str(data_set_1))

        return context
    

