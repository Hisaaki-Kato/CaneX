from django.shortcuts import render, redirect
from .models import Patient, Sharp
from django.db.models import Q
import pandas as pd
import numpy as np
import itertools
from io import TextIOWrapper, StringIO


def mainfunc(request):
    patients = Patient.objects.all()

    sites = sorted(set([patient.site for patient in patients]))
    p_TNMs = sorted(set([patient.p_TNM for patient in patients]))

    if request.method == 'POST':
        site_names = []
        p_TNM_names = []
        
        params = dict(request.POST)
        if 'site_settings' in request.POST:
            site_names = params['site_settings']
        if 'p_TNM_settings' in request.POST:
            p_TNM_names = params['p_TNM_settings']

        patients = Patient.objects.filter(Q(site__in=site_names) & Q(p_TNM__in=p_TNM_names))

    else:
        site_names = sites
        p_TNM_names = p_TNMs

    ids = []
    for patient in patients:
        ids.append(patient.number-1)

    sharps = Sharp.objects.all()

    node_list = []
    for i in itertools.permutations(sharps, r=2):
        vec1 = [int(num1) for num1 in i[0].vectors]
        vec2 = [int(num2) for num2 in i[1].vectors]
        dot = (np.dot(np.array(vec1)[ids], np.array(vec2)[ids]))
        dot_list = [i[0].name, i[1].name, dot]
        node_list.append(dot_list)

    count_list = []
    for n in sharps:
        vec = [int(num) for num in n.vectors]
        count = sum(np.array(vec)[ids])
        count_list.append([n.name, count])
    count_list = np.array(count_list)
    counts = (count_list[:,1]).astype(float)
    count_list[:,1] = counts/(counts.max()/100)

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