from django.shortcuts import render, redirect
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

# Create your views here.

night_colors = ['rgb(56, 75, 126)', 'rgb(18, 36, 37)', 'rgb(34, 53, 101)',
                'rgb(36, 55, 57)', 'rgb(6, 4, 4)']

def hello(request):
    df = pd.read_excel("D:\\Neptune\\Sales- Dashboard.xlsx")
    regions = ['Central', 'East', 'South', 'West']
    sales_by_region = []
    for i in regions:
        sales_by_region.append(df.loc[df['Region'] == i, 'Sales'].sum())
    fig = go.Figure(data=[go.Pie(labels=regions, values=sales_by_region, marker_colors=night_colors)])

    fig.update_layout(
        paper_bgcolor="LightSteelBlue",
        #paper_bgcolor="#0e0f2e",
        plot_bgcolor="#0e0f2e",
        margin=dict(l=20, r=20, t=20, b=20),
        width=500,
        height=500
    )
    '''
    fig.add_trace(
        go.Pie(df['Region'], values=sales_by_region, names=regions,
            color_discrete_sequence=px.colors.sequential.ice,
            template="plotly_dark"
        )
    )
    fig = px.pie(df['Region'], values=sales_by_region, names=regions,
                color_discrete_sequence=px.colors.sequential.ice,
                template="plotly_dark")
    fig2 = 
    '''
    div = fig.to_html(full_html=False)
    context = {'pie': div}
    return render(request, 'home.html', context)
