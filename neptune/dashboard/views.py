from django.shortcuts import render, redirect
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

# Create your views here.

night_colors = ['rgb(56, 75, 126)', 'rgb(18, 36, 37)', 'rgb(34, 53, 101)',
                'rgb(36, 55, 57)', 'rgb(6, 4, 4)']

master_width = 1000
master_height = 500

def hello(request):
    df = pd.read_excel("D:\\Neptune\\Sales- Dashboard.xlsx")


    #Pie chart
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
    #Bar chart
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
    fig1 = go.Figure()
    fig1.add_trace(
        go.Bar(
            x=sorted_sales_by_region,
            y=sorted_region_1,
            orientation='h',
            visible=True
        )
    )
    fig1.add_trace(
        go.Bar(
            x=sorted_sales_by_region_qty,
            y=sorted_region_2,
            orientation='h',
            visible=False
        )
    )

    buttons1 = [
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

    #Line chart

    sale_monthly = go.Figure()
    sale_qtr = go.Figure()

    months = ["0"+str(i) for i in range(1, 10)]
    months += ["10", "11", "12"]
    sales_by_month = []
    #regions = ['Central', 'East', 'South', 'West']
    sales_categorized = [[], [], [], []]
    for i in months:
        sales_by_month.append(df.loc[df['Order Date'].astype(str).str.contains("-"+i+"-"), 'Sales'].sum())
    sales_by_quarter = []
    sales_by_quarter.append(sales_by_month[0] + sales_by_month[1] + sales_by_month[2])
    sales_by_quarter.append(sales_by_month[3] + sales_by_month[4] + sales_by_month[5])
    sales_by_quarter.append(sales_by_month[6] + sales_by_month[7] + sales_by_month[8])
    sales_by_quarter.append(sales_by_month[9] + sales_by_month[10] + sales_by_month[11])
    quarters = ['I', 'II', 'III', 'IV']
    sales_categorized_qtr = [[], [], [], []]
    quarterly_count = 0
    for i in range(len(regions)):
        for j in months:
            value = df.loc[df['Order Date'].astype(str).str.contains("-"+j+"-") & (df['Region'] == regions[i]), 'Sales'].sum()
            sales_categorized[i].append(value)
            quarterly_count += value
            month_int = int(j)
            if(month_int % 3 == 0):
                sales_categorized_qtr[i].append(quarterly_count)
                quarterly_count = 0
    sale_monthly.add_trace(
        go.Scatter(
            x = months,
            y = sales_by_month,
            fill = 'tozeroy',
            visible = True
        )
    )
    sale_monthly.add_trace(
        go.Scatter(
            x = months,
            y = sales_categorized[0],
            fill = 'tozeroy',
            visible = False
        )
    )
    sale_monthly.add_trace(
        go.Scatter(
            x = months,
            y = sales_categorized[1],
            fill = 'tozeroy',
            visible = False
        )
    )
    sale_monthly.add_trace(
        go.Scatter(
            x = months,
            y = sales_categorized[2],
            fill = 'tozeroy',
            visible = False
        )
    )
    sale_monthly.add_trace(
        go.Scatter(
            x = months,
            y = sales_categorized[3],
            fill = 'tozeroy',
            visible = False
        )
    )
    sale_qtr.add_trace(
        go.Scatter(
            x = quarters,
            y = sales_by_quarter,
            fill = 'tozeroy',
            visible=True
        )
    )
    sale_qtr.add_trace(
        go.Scatter(
            x = quarters,
            y = sales_categorized_qtr[0],
            fill = 'tozeroy',
            visible = False
        )
    )
    sale_qtr.add_trace(
        go.Scatter(
            x = quarters,
            y = sales_categorized_qtr[1],
            fill = 'tozeroy',
            visible = False
        )
    )
    sale_qtr.add_trace(
        go.Scatter(
            x = quarters,
            y = sales_categorized_qtr[2],
            fill = 'tozeroy',
            visible = False
        )
    )
    sale_qtr.add_trace(
        go.Scatter(
            x = quarters,
            y = sales_categorized_qtr[3],
            fill = 'tozeroy',
            visible = False
        )
    )

    vis_matrix = [
        [],
        [],
        [],
        [],
        []
    ]

    for i in range(len(vis_matrix)):
        for x in range(5):
            if(x == i) :
                vis_matrix[i].append(True)
            else:
                vis_matrix[i].append(False)
    buttons1 = [
        dict(
            label='All',
            method='update',
            args=[{'visible': vis_matrix[0]}, {'title': 'All'}]
        ),
        dict(
            label='Central',
            method='update',
            args=[{'visible': vis_matrix[1]}, {'title': 'Central'}]
        ),
        dict(
            label='East',
            method='update',
            args=[{'visible': vis_matrix[2]}, {'title': 'East'}]
        ),
        dict(
            label='South',
            method='update',
            args=[{'visible': vis_matrix[3]}, {'title': 'South'}]
        ),
        dict(
            label='West',
            method='update',
            args=[{'visible': vis_matrix[4]}, {'title': 'West'}]
        )
    ]


    buttons2 = [
        dict(
            label='All',
            method='update',
            args=[{'visible': vis_matrix[0]}, {'title': 'All'}]
        ),
        dict(
            label='Central',
            method='update',
            args=[{'visible': vis_matrix[1]}, {'title': 'Central'}]
        ),
        dict(
            label='East',
            method='update',
            args=[{'visible': vis_matrix[2]}, {'title': 'East'}]
        ),
        dict(
            label='South',
            method='update',
            args=[{'visible': vis_matrix[3]}, {'title': 'South'}]
        ),
        dict(
            label='West',
            method='update',
            args=[{'visible': vis_matrix[4]}, {'title': 'West'}]
        )
    ]

    sale_monthly.update_layout(
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

    sale_qtr.update_layout(
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
    fig2 = go.Figure()
    df1 = pd.read_excel("D:\\Neptune\\Sales- Dashboard.xlsx", sheet_name="Returns")
    total_sales_count = df.shape[0]
    total_return_count = df1.shape[0]
    stages = ["Sale Initiated", "Sale Completed without a return"]
    funnel_data = [[total_sales_count, (total_sales_count-total_return_count)]]
    fig2.add_trace(
        go.Funnel(
        x = funnel_data[0],
        y = stages
        )
    )
    for i in range(len(regions)):
        total_sales_count = len(df[(df['Region'] == regions[i])])
        total_return_count = len(df[(df['Region'] == regions[i]) & (df['Order ID'].to_string() in df1['Order ID'].tolist())])
        funnel_data.append([total_sales_count, (total_sales_count-total_return_count)])
        fig2.add_trace(
           go.Funnel(
           x = funnel_data[i+1],
           y = stages
           )
        )

    buttons3 = [
        dict(
            label='All',
            method='update',
            args=[{'visible': vis_matrix[0]}, {'title': 'All'}]
        ),
        dict(
            label='Central',
            method='update',
            args=[{'visible': vis_matrix[1]}, {'title': 'Central'}]
        ),
        dict(
            label='East',
            method='update',
            args=[{'visible': vis_matrix[2]}, {'title': 'East'}]
        ),
        dict(
            label='South',
            method='update',
            args=[{'visible': vis_matrix[3]}, {'title': 'South'}]
        ),
        dict(
            label='West',
            method='update',
            args=[{'visible': vis_matrix[4]}, {'title': 'West'}]
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
                buttons=buttons3,
                showactive=True,
                x=0.15,
                xanchor='left',
                y=1.15,
                yanchor='top'
            )
        ]
    )

    div = fig.to_html(full_html=False)
    div1 = fig1.to_html(full_html=False)
    div2 = sale_monthly.to_html(full_html=False)
    div3 = sale_qtr.to_html(full_html=False)
    div4 = fig2.to_html(full_html=False)

    context = {'pie': div, 'bar': div1, 'sale_monthly': div2, 'sale_qtr': div3, 'funnel': div4}
    return render(request, 'home.html', context)
