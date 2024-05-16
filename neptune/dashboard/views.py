from django.shortcuts import render, redirect
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

# Create your views here.

night_colors = ['rgb(56, 75, 126)', 'rgb(18, 36, 37)', 'rgb(34, 53, 101)',
                'rgb(36, 55, 57)', 'rgb(6, 4, 4)']

master_width = 1000
master_height = 500

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
        width=master_width,
        height=master_height
    )

    fig1 = go.Figure()
    months = ["0"+str(i) for i in range(1, 10)]
    months += ["10", "11", "12"]
    sales_by_month = []
    for i in months:
        sales_by_month.append(df.loc[df['Order Date'].astype(str).str.contains("-"+i+"-"), 'Sales'].sum())
    sales_by_quarter = []
    sales_by_quarter.append(sales_by_month[0] + sales_by_month[1] + sales_by_month[2])
    sales_by_quarter.append(sales_by_month[3] + sales_by_month[4] + sales_by_month[5])
    sales_by_quarter.append(sales_by_month[6] + sales_by_month[7] + sales_by_month[8])
    sales_by_quarter.append(sales_by_month[9] + sales_by_month[10] + sales_by_month[11])
    quarters = ['I', 'II', 'III', 'IV']
    fig1.add_trace(
        go.Scatter(
            x = months,
            y = sales_by_month,
            fill = 'tozeroy',
            visible=True
        )
    )
    fig1.add_trace(
        go.Scatter(
            x = quarters,
            y = sales_by_quarter,
            fill = 'tozeroy',
            visible=False
        )
    )

    buttons1 = [
        dict(
            label='View by Month',
            method='update',
            args=[{'visible': [True, False]}, {'title': 'Monthly Sales'}]
        ),
        dict(
            label='View by Quarter',
            method='update',
            args=[{'visible': [False, True]}, {'title': 'Quarterly Sales'}]
        )
    ]

    fig1.update_layout(
        paper_bgcolor="LightSteelBlue",
        #paper_bgcolor="#0e0f2e",
        plot_bgcolor="#0e0f2e",
        margin=dict(l=20, r=20, t=20, b=20),
        width=master_width,
        height=master_height,
        updatemenus=[
            dict(
                type='buttons',
                direction='right',
                buttons=buttons1,
                showactive=True,
                x=0.15,
                xanchor='left',
                y=1.15,
                yanchor='top'
            )
        ]
    )

    sales_by_region_qty = []
    for i in regions:
        sales_by_region_qty.append(df.loc[df['Region'] == i, 'Quantity ordered new'].sum())
    temp = [[sales_by_region[i], regions[i]] for i in range(4)]
    temp = sorted(temp)
    sorted_sales_by_region = [temp[i][0] for i in range(4)]
    sorted_region_1 = [temp[i][1] for i in range(4)]
    temp = [[sales_by_region_qty[i], regions[i]] for i in range(4)]
    temp = sorted(temp)
    sorted_sales_by_region_qty = [temp[i][0] for i in range(4)]
    sorted_region_2 = [temp[i][1] for i in range(4)]
    fig2 = go.Figure()
    fig2.add_trace(
        go.Bar(
            x=sorted_sales_by_region,
            y=sorted_region_1,
            orientation='h',
            visible=True
        )
    )
    fig2.add_trace(
        go.Bar(
            x=sorted_sales_by_region_qty,
            y=sorted_region_2,
            orientation='h',
            visible=False
        )
    )

    buttons2 = [
        dict(
            label='View by Revenue',
            method='update',
            args=[{'visible': [True, False]}, {'title': 'Revenue'}]
        ),
        dict(
            label='View by Quantity',
            method='update',
            args=[{'visible': [False, True]}, {'title': 'Quantity'}]
        )
    ]

    fig2.update_layout(
        paper_bgcolor="LightSteelBlue",
        #paper_bgcolor="#0e0f2e",
        plot_bgcolor="#0e0f2e",
        margin=dict(l=20, r=20, t=20, b=20),
        width=master_width,
        height=master_height,
        updatemenus=[
            dict(
                type='buttons',
                direction='right',
                buttons=buttons2,
                showactive=True,
                x=0.15,
                xanchor='left',
                y=1.15,
                yanchor='top'
            )
        ]
    )

    # Funnel
    
    df1 = pd.read_excel("D:\\Neptune\\Sales- Dashboard.xlsx", sheet_name="Returns")
    total_sales_count = df.shape[0]
    total_return_count = df1.shape[0]
    stages = ["Sale Initiated", "Sale Completed without a return"]
    fig3 = go.Figure()
    fig3.add_trace(go.Funnel(
        x = [total_sales_count, (total_sales_count-total_return_count)],
        y = stages
    ))

    fig3.update_layout(
        paper_bgcolor="LightSteelBlue",
        #paper_bgcolor="#0e0f2e",
        plot_bgcolor="#0e0f2e",
        margin=dict(l=20, r=20, t=20, b=20),
        width=master_width,
        height=master_height
    )


    div = fig.to_html(full_html=False)
    div1 = fig1.to_html(full_html=False)
    div2 = fig2.to_html(full_html=False)
    div3 = fig3.to_html(full_html=False)

    context = {'pie': div, 'trend': div1, 'bar': div2, 'funnel': div3}
    return render(request, 'home.html', context)
