# Copyright 2022 British Broadcasting Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from sanic import Sanic
from sanic.response import json
from sanic.exceptions import SanicException
from carbon_minimiser.minimiser_api.minimiser import Minimiser
from carbon_minimiser.carbon_api.carbon_api_wrapper.carbon import REGIONS
import carbon_minimiser.config as CONFIG

LOCATIONS = CONFIG.locations

def round_to_half_int(number):
    return round(number * 2) / 2

def get_num_results(request):
    try:
        results = int(request.args['results'][0])
    except KeyError:
        results = 1
    except ValueError:
        raise SanicException("Bad Request, are your arguments formatted correctly?", status_code=400)
    return results


def get_time_range(request):
    try:
        range_param = request.args['range'][0].split(",")
        range = [round_to_half_int(float(r)) for r in range_param]
        if range[0] > range [1]:
            raise ValueError
    except KeyError:
        range = [0,95]
    except ValueError:
        raise SanicException("Bad Request, are your arguments formatted correctly?", status_code=400)
    return range

def limit_results(num_results, time_range):
    max_results = int((time_range[1] - time_range[0])*2)
    return num_results if num_results < max_results else max_results


def create_app():
    app = Sanic("Carbon_Minimiser")
    min = Minimiser()
    min.set_cache(True, CONFIG.cache_refresh) if CONFIG.cache else min.set_cache(False)
    attach_endpoints(app, min)
    return app


def attach_endpoints(app, min):
    @app.get('/')
    async def root(request):
        return json("Carbon Minimiser")


    @app.get('/timestamp')
    async def timestamp(request):
        try:
            result = await min.cache_timestamp() 
        except KeyError:
            result = "Cache not found"
        return json(result)


    @app.get('/optimise')
    async def optimal_time_and_location(request):
        time_range = get_time_range(request)
        num_results = limit_results(get_num_results(request), time_range)
        result = await min.optimal_time_and_location(LOCATIONS, num_options=num_results, time_range=time_range)
        return json(result)


    @app.get('/optimise/location')
    async def optimal_location(request):
        result = await min.optimal_location_now(LOCATIONS)
        return json(result)


    @app.get('/optimise/location/<location>')
    async def optimal_time_for_location(request, location):
        location = location.upper()
        time_range = get_time_range(request)
        num_results = limit_results(get_num_results(request), time_range)
        if location in LOCATIONS:
            result = await min.optimal_time_for_location(location, num_options=num_results, time_range=time_range)
            return json(result)
        else:
            return json("Location not configured", 404)


    @app.get('/optimise/location/<location>/window/<window:float>')
    async def optimal_time_window_for_location(request, location, window):
        location = location.upper()
        time_range = get_time_range(request)
        num_results = limit_results(get_num_results(request), time_range)
        if location in LOCATIONS:
            result = await min.optimal_time_window_for_location(location, 
                                                                window, 
                                                                num_options=num_results,
                                                                time_range=time_range)
            return json(result)
        else:
            return json("Location not configured", 404)


    @app.get('/optimise/location/window/<window:float>')
    async def optimal_time_window_and_location(request, window):
        time_range = get_time_range(request)
        num_results = limit_results(get_num_results(request), time_range)
        result = await min.optimal_time_window_and_location(LOCATIONS, window, num_options=num_results, time_range=time_range)
        return json(result)
