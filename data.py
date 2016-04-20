import json
import sys
#bar graph imports
import plotly as plot
import plotly.graph_objs as go

__author__ = 'Andrew Watts'
__version__ = '1.01'
__Python__ = '2.7.11'
__Email__ = 'wattsap@appstate.edu'
__usage__ = 'python filename.py json-filename'
'''
- SOURCE LINKS:
- https://plot.ly/python/getting-started/
- https://plot.ly/python/bar-charts/
'''


class data:
    '''
    @Function init: builds data model
    @param filename: json file to load
    '''

    def __init__(self, filename):
        with open(filename, 'r') as fp:
            self.data = json.load(fp)
            self.county_data = {}
            self.most_alcohol = 0
            self.most_alcohol_county_idx = ''
            self.x = []
            self.x_names = []
            self.y = []

    '''
    @function county_volume: creates a dictionary of county numbers
    and total alcohol purchases by milliliter
    '''

    def county_volume(self):
        #county_data = {}
        for i in self.data:
            self.county_data[str(i['county_number'])] = 0
        for i in self.data:
            self.county_data[str(i['county_number'])] += int(i[
                'bottle_volume_ml'])
        #print(county_data)

    '''
    @function county_most: finds the county with the most alcohol
    consumption and sets the self county alcohol amount and the self
    county alcohol index tags to the county that purchases the most
    alcohol for the data set
    '''

    def county_most(self):
        #most = 0
        #most_idx = ''
        for i, j in self.county_data.items():
            if j > self.most_alcohol:
                self.most_alcohol = j
            if self.most_alcohol == j:
                self.most_alcohol_county_idx = i

    '''
    @function get_most_country_name: gets the county name that purchased the
    most alcohol
    '''

    def get_most_county_name(self):
        for i in self.data:
            if int(i['county_number']) == int(self.most_alcohol_county_idx):
                return i['county']
        return 'No county matching county ID number.'

    '''
    @function test: shitty testing suite. Dont care much right now how clean
    it looks
    '''

    def test(self):
        self.county_volume()
        self.county_most()
        print('Data by county: ')
        print(self.county_data)
        print('\n\n')
        print(
            'The most alcohol was ordered in county name: %s id: %s, with an order amount of: %d ml'
            % (self.get_most_county_name(), self.most_alcohol_county_idx,
               self.most_alcohol))
        print('\n\n')
        self.prep_graph()
        self.bar_graph()

    '''
    create x and y lists for graphing, and save in self x and y tags
    '''

    def prep_graph(self):
        for i, j in self.county_data.items():
            self.x.append(i)
            self.y.append(j)

    '''
    create bar graph with self x and y data
    '''

    def bar_graph(self):
        info = [
            go.Bar(
                x=self.x,
                y=self.y,
                #work on different colored graphs
                #marker=dict(color=['rgba(222,45,38,0.8)' * len(self.x)],)
            )
        ]
        layout = go.Layout(title='Alcohol Purchase by County In Iowa', )
        fig = go.Figure(data=info, layout=layout)
        #offline tag critical, online is paid repo service
        #offline saves local html and opens it
        plot.offline.plot(fig, filename='County Alcohol Sales')


if len(sys.argv) == 2:
    d = data(sys.argv[1])
else:
    d = raw_input('Enter filename: ')
d.test()
