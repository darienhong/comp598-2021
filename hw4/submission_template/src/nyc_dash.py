# python application for bokeh dashboard 
import json
from bokeh.layouts import column, row
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Dropdown, Legend, LegendItem
from bokeh.models.tickers import SingleIntervalTicker
from bokeh.core.properties import Color


# load data 
with open('processed_data.json', 'r') as file: 
    processed_data = json.load(file)

unique_zips = processed_data[0]
zip_info = processed_data[1]
monthly_avg = processed_data[2]

# constant vars  
c1 = '#A4D3E8'
c2 = '#F4E98D'
c3 = '#E8A4B1'
xs = [[*range(0,12)], [*range(0,12)], [*range(0,12)]]
ys = [[0]*12, [0]*12, monthly_avg]

# authentication with URL query 
def authenticate(curdoc): 
    url_args = curdoc.session_context.request.arguments 
    username = url_args.get('username')[0].decode('utf-8')
    password = url_args.get('password')[0].decode('utf-8')

    if username != 'nyc': 
        raise Exception('Incorrect Username, cannot access dashboard')

    if password != 'iheartnyc':
        raise Exception('Incorrect Password, cannot access dashboard')


# hosting data and GUI 
def update_1(event): 
    source_n = zip_info[event.item]
    source.data = dict(colors=[c1, c2, c3], xs=xs, ys=[source_n, source.data['ys'][1], monthly_avg])
    plot.y_range.start = 0 
    # y axis ends at max 
    plot.y_range.end = max(max(source_n), max(source.data['ys'][1]), max(monthly_avg))


def update_2(event): 
    source_n = zip_info[event.item]
    source.data = dict(colors=[c1, c2, c3], xs=xs, ys=[source.data['ys'][0], source_n, monthly_avg])
    plot.y_range.start = 0 
    # y axis ends at max 
    plot.y_range.end = max(max(source.data['ys'][0]), max(source_n), max(monthly_avg))

# dropdown UI
dropdown1 = Dropdown(label="Zipcode 1", button_type="primary", menu=unique_zips)
dropdown2 = Dropdown(label="Zipcode 2", button_type="warning", menu=unique_zips)
dropdown1.on_click(update_1)
dropdown2.on_click(update_2)

# server 
curr_doc = curdoc() 
curr_doc.title = 'Response Time to Complaints by Zipcode'
authenticate(curr_doc)

# plot
source = ColumnDataSource(dict(colors=[c1, c2, c3], xs=xs, ys=ys, labels=['Zipcode 1', 'Zipcode 2', 'ALL 2020']))
plot = figure(x_range=(0, 12), x_axis_label='Months', y_axis_label='Average Duration (h)', title="Response Time")
plot.multi_line(xs='xs', ys='ys', line_color='colors', legend_group='labels', source=source)
plot.xaxis.ticker = SingleIntervalTicker(interval=1)
plot.xaxis.minor_tick_line_color = None
plot.y_range.start = 0

# load dashboard 
curr_doc.theme = 'contrast'
curr_doc.add_root(row(column(dropdown1, dropdown2), plot))