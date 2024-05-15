from django.shortcuts import render, redirect
import plotly.express as px 
import numpy as np
import pandas as pd

# Create your views here.

def hello(request):
    df = pd.read_excel("D:\\Neptune\\Sales- Dashboard.xlsx")
    region_labels = ['Central', 'East', 'South', 'West']
    values = []
    for i in region_labels:
        values.append(df.loc[df['Region'] == i, 'Sales'].sum())
    fig = pgo.pie(df['Region'], values=values, names=region_labels)
    div = fig.to_html(full_html=False)
    context = {'pie': div}
    return render(request, 'home.html', context);
