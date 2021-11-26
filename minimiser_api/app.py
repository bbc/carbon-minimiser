from sanic import Sanic
from sanic.response import json
from minimiser_api.minimiser import Minimiser
from carbon_api.carbon_api_wrapper.carbon import REGIONS

app = Sanic("Carbon Minimiser")
min = Minimiser()
locations = ['N_SCOTLAND', 'S_SCOTLAND', 'NW_ENGLAND', 'NE_ENGLAND', 'YORKSHIRE',
             'N_WALES', 'S_WALES', 'W_MIDLANDS', 'E_MIDLANDS', 'E_ENGLAND', 'SW_ENGLAND',
             'S_ENGLAND', 'LONDON', 'SE_ENGLAND', 'ENGLAND', 'SCOTLAND', 'WALES']


def get_num_results(request):
    try:
        results = int(request.args['results'][0])
    except KeyError:
        results = 1
    return results


def get_time_range(request):
    try:
        range_param = request.args['range'][0].split(",")
        range = [float(r) for r in range_param]
    except KeyError:
        range = [0,95]
    return range


@app.get('/')
async def root(request):
    return json("Carbon Minimiser")


@app.get('/optimise')
async def optimal_time_and_location(request):
    result = await min.optimal_time_and_location(locations, num_options=get_num_results(request), time_range=get_time_range(request))
    return json(result)


@app.get('/optimise/location')
async def optimal_location(request):
    result = await min.optimal_location_now(locations)
    return json(result)


@app.get('/optimise/location/<location>')
async def optimal_time_for_location(request, location):
    location = location.upper()
    if location in REGIONS.keys():
        result = await min.optimal_time_for_location(location, num_options=get_num_results(request), time_range=get_time_range(request))
        return json(result)
    else:
        return json("Location not found", 404)


@app.get('/optimise/location/<location>/window/<window:number>')
async def optimal_time_window_for_location(request, location, window):
    location = location.upper()
    if location in REGIONS.keys():
        result = await min.optimal_time_window_for_location(location, 
                                                            window, 
                                                            num_options=get_num_results(request),
                                                            time_range=get_time_range(request))
        return json(result)
    else:
        return json("Location not found", 404)


@app.get('/optimise/location/window/<window:number>')
async def optimal_time_window_and_location(request, window):
    result = await min.optimal_time_window_and_location(locations, window, num_options=get_num_results(request), time_range=get_time_range(request))
    return json(result)
