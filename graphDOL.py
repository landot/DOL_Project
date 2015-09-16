__author__ = 'timl'

import plotly.plotly as py
from plotly.graph_objs import *

import pymongo

# Connection to Mongo DB
try:
    conn = pymongo.MongoClient('localhost', 27017)
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e
   conn
db = conn['test-database4']

#test
officeName = ['Bellevue/Bel-Red']

#'Bellingham', 'Bremerton', 'Kennewick', 'Lacey', 'Lynnwood',
 #           'Mount Vernon', 'Parkland', 'Puyallup', 'Renton', 'Seattle: Downtown',
  #          'Seattle: West Seattle', 'Smokey Point', 'Spokane', 'Tacoma', 'Union Gap', 'Vancouver-North', 'Wenatchee'


py.sign_in('timowland', 'uw95g37quk')
for office in officeName:
    #titleHeader = 'DOL Wait Times in ' + office
    labels = ['New Drivers License', 'Drivers License Renewal']

    colors = ['#008B45', '#7D9EC0']

    mode_size = [8,8]

    line_size = (2,2)

    x_data = [[],[]]
    #will be new license [[], (TOD)
    #then   renew license []] (TOD)

    y_data = [[],[]]
    #will be new license [[], (wait time)
    # then renew license  []] (wait time)


    for obj in db.test.alldol.find({'Location:': office}):
        if obj['Timestamp'].strftime("%m %d") == "09 15":
            x_data[0].append(obj['Timestamp'].strftime("%H:%M"))
            x_data[1].append(obj['Timestamp'].strftime("%H:%M"))
            y_data[0].append(obj['New License Wait Time:'])
            y_data[1].append(obj['License Renewal Wait Time:'])

    print x_data
    print y_data

    traces = []

    for i in range(0, 2):
        lineName = ''
        if i == 0:
            lineName = 'License (New)'
        else:
            lineName = 'License Renewal'
        traces.append(Scatter(
            x=x_data[i],
            y=y_data[i],
            mode='lines',
            name=lineName,
            line=Line(color=colors[i], width=line_size[i]),
            connectgaps=True,
        ))



        '''traces.append(Scatter(
            x=[x_data[i][0], x_data[i][len(x_data[0]) - 1]],
            y=[y_data[i][0], y_data[i][len(x_data[0]) - 1]],
#            mode='lines',
            name=lineName,
            marker=Marker(color=colors[i], size=mode_size[i])
        ))'''



    layout = Layout(
        xaxis=XAxis(
            title='Time of Day',
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            autotick=False,
            ticks='outside',
            tick0 = 930,
            dtick = 30,
            tickcolor='rgb(204, 204, 204)',
            tickwidth=2,
            ticklen=5,
            tickfont=Font(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=YAxis(
            title='Wait Time (minutes)',
            showgrid=True,
            zeroline=True,
            showline=True,
            showticklabels=True,
        ),
        height=600,
        width=600,
        autosize=False,
        margin=Margin(
            autoexpand=False,
            l=100,
            r=20,
            t=110,
        ),
        showlegend=True,
        legend=Legend(
            x=0,
            y=1,
            traceorder='normal',
            font=Font(
                family='sans-serif',
                size=12,
                color='#000'
            ),
            bgcolor='#E2E2E2',
            bordercolor='#FFFFFF',
            borderwidth=2
    )
    )

    annotations = []

    # Adding labels
    for y_trace, label, color in zip(y_data, labels, colors):

        # labeling the left_side of the plot
        '''annotations.append(Annotation(xref='paper', x=0.05, y=y_trace[0],
                                      xanchor='right', yanchor='middle',
                                      text=label + ' {}'.format(y_trace[0]),
                                      font=Font(family='Arial',
                                                size=16,
                                                color=colors,),
                                      showarrow=False,))'''
        # labeling the right_side of the plot
        '''annotations.append(Annotation(xref='paper', x=0.95, y=y_trace[len(x_data[0]) - 1],
                                      xanchor='left', yanchor='middle',
                                      text='{}'.format(y_trace[len(x_data[0]) - 1]),
                                      font=Font(family='Arial',
                                                size=50,
                                                color=colors,),
                                      showarrow=False,))'''
    # Title
    annotations.append(Annotation(xref='paper', yref='paper', x=0.0, y=1.05,
                                  xanchor='left', yanchor='bottom',
                                  text='DOL Wait Times in ' + office,
                                  font=Font(family='Arial',
                                            size=24,
                                            color='rgb(37,37,37)'),
                                  showarrow=False,))
    # Source
    '''annotations.append(Annotation(xref='paper', yref='paper', x=0.5, y=-0.1,
                                  xanchor='center', yanchor='top',
                                  text='',
                                  font=Font(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                  showarrow=False,))'''

    layout['annotations'] = annotations

    fig = Figure(data=traces, layout=layout)
    plot_url = py.plot(fig, filename= (office + ' test 3'))
