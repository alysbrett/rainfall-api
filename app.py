"""
REST API demo for PyCon UK Science Track
For demonstration purposes only!
"""

#Modules to create API and web application
from flask import Flask, make_response
from flask_restful import Api, Resource, abort

#Modules to get and plot data
from plot import rainfall_bar_chart
import data as datasource

#First part of URLs - API name and version
BASE_ROUTE = "/rainfall-api/v1"
MESSAGE_NOT_FOUND = "Data not found for this year"

#Create Flask app
app = Flask(__name__)
api = Api(app)


# Define Resource classes

class YearList(Resource):

    """ Just lists links to individual years (json)"""

    def get(self):

        #Make list of links to individual years
        year_list = []
        for row in datasource.get_data():
            year = row[0]
            year_list.append("{}/years/{}".format(BASE_ROUTE, year))

        response_data = {
            "links":{
                "root":BASE_ROUTE,
                "next":year_list
            }
        }

        return response_data


class Year(Resource):

    """ Total annual rainfall and links to
    resources for monthly data and plot (json) """

    def get(self, year):

        data = datasource.get_year_data(year)
        if data is None:
            abort(404, message=MESSAGE_NOT_FOUND)

        total = sum(data)

        response_data = {
            "links":{
                "root":BASE_ROUTE,
                "previous":"{}/years".format(BASE_ROUTE),
                "next":[
                    "{}/years/{}/data".format(BASE_ROUTE, year),
                    "{}/years/{}/plot".format(BASE_ROUTE, year)
                ]
            },
            "data":{
                "total-rainfall":total,
                "units":"mm"
            }
        }

        return response_data


class Data(Resource):

    """Monthly rainfall data (json) """

    def get(self, year):

        data = datasource.get_year_data_dict(year)
        months = datasource.get_month_labels()

        if data is None:
            abort(404, message=MESSAGE_NOT_FOUND)

        data_list = []
        for month in months:
            data_point_dict = {
                "month":month,
                "val":data[month]
            }
            data_list.append(data_point_dict)

        response_data = {
            "links":{
                "root":BASE_ROUTE,
                "previous":"{}/years/{}".format(BASE_ROUTE, year),
            },
            "data":{
                "values":data_list,
                "units":"mm"
            }
        }

        return response_data


class Plot(Resource):

    """ Bar chart of rainfall for year by month (png) """

    def get(self, year):

        vals = datasource.get_year_data(year)
        labels = datasource.get_month_labels()
        title = "{} monthly rainfall".format(year)

        if vals is None:
            abort(404, message=MESSAGE_NOT_FOUND)

        bytestream = rainfall_bar_chart(vals, labels, title)

        # assemble response
        response = make_response(bytestream.getvalue())
        response.headers["Content-Type"] = "image/png"

        return response


# Map resource classes onto URLs

api.add_resource(YearList, BASE_ROUTE + "/years")
api.add_resource(Year, BASE_ROUTE + "/years/<int:year>")
api.add_resource(Plot, BASE_ROUTE + "/years/<int:year>/plot")
api.add_resource(Data, BASE_ROUTE + "/years/<int:year>/data")

# Start web app

if __name__ == "__main__":
    app.run(host='localhost', debug=True)
