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
from carbon_minimiser.carbon_api.carbon_api_wrapper.carbon import CarbonAPI
from carbon_minimiser.minimiser_api.cache import Cache
from itertools import islice
from typing import List
import threading

class Minimiser:
    def __init__(self):
        self.api = CarbonAPI()

    def set_cache(self, cache, refresh_rate=None):
        self.cache = Cache(refresh_rate) if cache else False
        if cache:
            thread = threading.Thread(target=self.cache.start_caching, daemon=True)
            thread.start()

    @staticmethod
    def _window(seq: List, n: int):
        """
        :return: Returns a sliding window (of width n) over data from the iterable
        s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...
        from: https://stackoverflow.com/questions/6822725/rolling-or-sliding-window-iterator
        """
        it = iter(seq)
        result = tuple(islice(it, n))
        if len(result) == n:
            yield result
        for elem in it:
            result = result[1:] + (elem,)
            yield result
    
    async def cache_timestamp(self):
        return self.cache.get('created')

    async def optimal_location_now(self, locations: List[str]):
        """
        Given a list of locations, returns the location with lowest carbon intensity right now
        :param locations: list of locations, see carbon_api_wrapper.carbon.REGIONS
        :return: dict of optimal location, carbon cost, and carbon index
        """
        options = []
        for location in locations:
            if self.cache:
                intensity, index = self.cache.get("current_region_intensity")[location]
            else:
                intensity, index = await self.api.current_region_intensity(location)
            options.append({"location": location, "forecast": intensity, "index": index})
        sorted_locations = sorted(options, key=lambda x: x['forecast'])
        return sorted_locations[0]

    async def optimal_time_for_location(self, location: str, num_options: int = 1, time_range=[0, 47.5]):
        """
        Given a location, returns the lowest carbon intensity half hour within the given time range
        :param location: location string, see carbon_api_wrapper.carbon.REGIONS
        :param num_options: define the number of top options returned
        :return: dict containing optimal time, carbon forecast, carbon index, and location. List of dicts if num_options > 1
        """
        if self.cache:
            times = self.cache.get("region_forecast_range")[f"('{location}', 47.5)"]
        else:
            times = await self.api.region_forecast_range(location, time_range[1])
        # cut off times outside of time range
        times = times[int(time_range[0]*2):int(time_range[1])*2]
        sorted_times = sorted(times, key=lambda x: x['forecast'])
        optimal_times = sorted_times[0:num_options]
        return optimal_times[0] if len(optimal_times) == 1 else optimal_times

    async def optimal_time_and_location(self, locations: List[str], num_options: int = 1, time_range=[0, 47.5]):
        """
        Given a list of locations, returns the time and location of the lowest carbon
        intensity half hour window over the given time range
        :param locations: list of locations, see carbon_api.carbon_api_wrapper.carbon.REGIONS
        :param num_options: define the number of top options returned
        :param time_range: list defining start and end time range in hours from current time
        :return: dict of optimal time, carbon forecast, carbon index, optimal location. List of dicts if num_options > 1
        """
        options = []
        for location in locations:
            if self.cache:
                times = self.cache.get("region_forecast_range")[f"('{location}', 47.5)"]
            else:
                times = await self.api.region_forecast_range(location, 48)
            # cut off times outside of time range
            times = times[int(time_range[0]*2):int(time_range[1])*2]
            for time in times:
                # results don't come back with location attached
                time['location'] = location
            options = options + times
        sorted_options = sorted(options, key=lambda x: x['forecast'])
        optimal_options = sorted_options[0:num_options]
        return optimal_options[0] if len(optimal_options) == 1 else optimal_options

    async def optimal_time_window_for_location(self, location: str, window_len: float, num_options: int = 1, time_range=[0, 47.5]):
        """
        Given a location and time window, returns the start of the time window with lowest
        carbon intensity over the given time range in that location
        :param location: location string, see carbon_api.carbon_api_wrapper.carbon.REGIONS
        :param window_len: integer number of hours that you wish to optimise for
        :param num_options: define the number of top options returned
        :param time_range: list defining start and end time range in hours from current time
        :return: dict of optimal time, and average carbon forecast for window. List of dicts if num_options > 1
        """
        # request times up until max time range
        if self.cache:
            times = self.cache.get("region_forecast_range")[f"('{location}', 47.5)"]
        else:
            times = await self.api.region_forecast_range(location, time_range[1])
        # cut off times outside of time range
        times = times[int(time_range[0]*2):int(time_range[1])*2]
        costs = []
        # convert hours into half hours
        half_hours = int(window_len * 2) if window_len < 48 else 95
        for window in self._window(times, half_hours):
            carbon_cost = round(sum([f['forecast'] for f in window])/half_hours)
            cost = {'time': window[0]['time'], 'forecast': carbon_cost}
            costs.append(cost)
        sorted_times = sorted(costs, key=lambda x: x['forecast'])
        optimal_times = sorted_times[0:num_options]
        return optimal_times[0] if len(optimal_times) == 1 else optimal_times

    async def optimal_time_window_and_location(self, locations: List[str], window_len: float, num_options: int = 1, time_range=[0, 47.5]):
        """
        Given a list of locations and a time window, returns the location and start of the time window with lowest
        carbon intensity over the given time range
        :param locations: list of locations, see carbon_api.carbon_api_wrapper.carbon.REGIONS
        :param window_len: number of hours that you wish to optimise for
        :param num_options: define the number of top options returned
        :param time_range: list defining start and end time range in hours from current time
        :return: dict of optimal location, optimal time, and average carbon forecast for window. List of dicts if num_options > 1
        """
        costs = []
        for location in locations:
            if self.cache:
                times = self.cache.get("region_forecast_range")[f"('{location}', 47.5)"]
            else:
                times = await self.api.region_forecast_range(location, time_range[1])
            # cut off times outside of time range
            times = times[int(time_range[0]*2):int(time_range[1])*2]
            # convert hours into half hours
            half_hours = int(window_len * 2) if window_len < 48 else 95
            for window in self._window(times, half_hours):
                carbon_cost = round(sum([f['forecast'] for f in window])/half_hours)
                cost = {'location': location, 'time': window[0]['time'], 'forecast': carbon_cost}
                costs.append(cost)
        sorted_options = sorted(costs, key=lambda x: x['forecast'])
        optimal_options = sorted_options[0:num_options]
        return optimal_options[0] if len(optimal_options) == 1 else optimal_options
