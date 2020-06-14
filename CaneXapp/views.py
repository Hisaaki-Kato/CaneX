from django.shortcuts import render, redirect
from .models import Patient, Sharp
from django.db.models import Q
import pandas as pd
import numpy as np
import itertools
from io import TextIOWrapper, StringIO


def mainfunc(request):

    sites = sorted(set(Patient.objects.values_list('site', flat=True)))
    p_TNMs = sorted(set(Patient.objects.values_list('p_TNM', flat=True)))

    if request.method == 'POST':
        params = dict(request.POST)
        if ('site_settings' in request.POST) & ('p_TNM_settings' in request.POST):
            site_names = params['site_settings']
            p_TNM_names = params['p_TNM_settings']
            patients = Patient.objects.filter(Q(site__in=site_names) & Q(p_TNM__in=p_TNM_names))
        else:
            return render(request, 'main.html', {'sites': sites,
                                                 'p_TNMs': p_TNMs})

    else:
        patients = Patient.objects.all()
        site_names = sites
        p_TNM_names = p_TNMs

    patient_ids = patients.values_list('number', flat=True)

    sharp_names = Sharp.objects.values_list('name', flat=True)
    sharp_num = len(sharp_names)
    
    vec_txt = Sharp.objects.values_list('vectors', flat=True)
    vectors = np.array([[int(t) for t in txt] for txt in vec_txt])[:,patient_ids]

    node_list = []
    for i in itertools.permutations(range(sharp_num), r=2):
        dot = (np.dot(vectors[i[0]], vectors[i[1]]))
        dot_list = [sharp_names[i[0]], sharp_names[i[1]], dot]
        node_list.append(dot_list)

    max_count = max(np.sum(vectors, axis=1))
    count_list = []
    for n in range(sharp_num):
        count = sum(vectors[n])/(max_count/100)
        count_list.append([sharp_names[n], count])

    return render(request, 'main.html', {'sites': sites,
                                         'p_TNMs': p_TNMs,
                                         'count_list': count_list, 
                                         'node_list': node_list,
                                         'site_names': site_names,
                                         'p_TNM_names': p_TNM_names})


def uploadfunc(request):
    if request.method == 'GET':
        is_patient = bool(Patient.objects.first())
        return render(request, 'upload.html', {'is_patient': is_patient})

    elif request.method == 'POST':
        if 'patient_csv' in request.FILES:
            form_data = TextIOWrapper(request.FILES['patient_csv'].file, encoding='utf-8')
            data = pd.read_csv(form_data, index_col=0)

            for row in range(len(data)):
                patient, created = Patient.objects.get_or_create(name=data.index[row])
                patient.name = data.index[row]
                patient.site = data["Occupied site"][row]
                patient.p_TNM = data["p-TNM"][row]
                patient.number = row
                patient.save()

            for col in range(len(data.T)-2):
                sharp, created = Sharp.objects.get_or_create(name=data.columns[col])
                sharp.name = data.columns[col]
                sharp.vectors = ''.join([str(i) for i in data.iloc[:,col].tolist()])
                sharp.save()

            return render(request, 'upload.html', {'text': 'Successfully uploaded!'})
        else:
            return render(request, 'upload.html', {'text': 'ERROR!: please input ".npy" file!'})

    else:
        return render(request, 'upload.html')


def deletefunc(request):
    if request.method == 'POST':
        Patient.objects.all().delete()
        Sharp.objects.all().delete()
        return redirect('upload')

    return render(request, 'delete.html', {'text': 'Model all deleted!'})