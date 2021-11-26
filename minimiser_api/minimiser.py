from carbon_api.carbon_api_wrapper.carbon import CarbonAPI
from cache.cache import Cache
from itertools import islice
from typing import List


class Minimiser:
    def __init__(self, cache=True):
        self.api = CarbonAPI()
        cache = Cache(None)
        self.cache = cache.read_cache()

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

    async def optimal_location_now(self, locations: List[str]):
        """
        Given a list of locations, returns the location with lowest carbon intensity right now
        :param locations: list of locations, see carbon_api_wrapper.carbon.REGIONS
        :return: lowest carbon location (str)
        """
        options = []
        for location in locations:
            if self.cache:
                intensity, index = self.cache["current_region_intensity"][location]
            else:
                intensity, index = await self.api.current_region_intensity(location)
            options.append({"location": location, "cost": intensity, "index": index})
        sorted_locations = sorted(options, key=lambda x: x['cost'])
        return sorted_locations[0]

    async def optimal_time_for_location(self, location: str, num_options: int = 1, time_range=[0, 47.5]):
        """
        Given a location, returns the lowest carbon intensity half hour within the given time range
        :param location: location string, see carbon_api_wrapper.carbon.REGIONS
        :param num_options: define the number of top options returned
        :return: number of hours and mins till optimal time as +hh:mm string
        """
        if self.cache:
            times = self.cache["region_forecast_range"][f"('{location}', 47.5)"]
            # cut upper time range out of cache
            index = int(time_range[1]*2) if time_range[1] < 48 else 95
            times = times[0: index + 1]
        else:
            times = await self.api.region_forecast_range(location, time_range[1])
        # cut off times before min time range
        times = times[int(time_range[0]*2):]
        sorted_times = sorted(times, key=lambda x: x['forecast'])
        optimal_times = sorted_times[0:num_options]
        return optimal_times[0] if len(optimal_times) == 1 else optimal_times

    async def optimal_time_and_location(self, locations: List[str], num_options: int = 1, time_range=[0, 47.5]):
        """
        Given a list of locations, returns the time and location of the lowest carbon
        intensity half hour window over the given time range
        :param locations: list of locations, see carbon_api_wrapper.carbon.REGIONS
        :param num_options: define the number of top options returned
        :return: tuple of (location, time), where time is num hours until optimal start time in hh:mm
        """
        options = []
        for location in locations:
            if self.cache:
                times = self.cache["region_forecast_range"][f"('{location}', 47.5)"]
            else:
                times = await self.api.region_forecast_range(location, 48)
            # cut off times before min time range
            times = times[int(time_range[0]*2):]
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
        :param location: location string, see carbon_api_wrapper.carbon.REGIONS
        :param window_len: integer number of hours that you wish to optimise for
        :param num_options: define the number of top options returned
        :param time_range: list defining start and end time range in hours from current time
        :return: number of hours and mins from now as +hh:mm string
        """
        # request times up until max time range
        if self.cache:
            times = self.cache["region_forecast_range"][f"('{location}', 47.5)"]
            # cut upper time range out of cache
            index = int(time_range[1]*2) if time_range[1] < 48 else 95
            times = times[0: index + 1]
        else:
            times = await self.api.region_forecast_range(location, time_range[1])
        # cut off times before min time range
        times = times[int(time_range[0]*2):]
        costs = []
        # convert hours into half hours
        half_hours = int(window_len * 2) if window_len < 48 else 95
        for window in self._window(times, half_hours):
            carbon_cost = sum([f['forecast'] for f in window])
            cost = {'time': window[0]['time'], 'cost': carbon_cost}
            costs.append(cost)
        sorted_times = sorted(costs, key=lambda x: x['cost'])
        optimal_times = sorted_times[0:num_options]
        return optimal_times[0] if len(optimal_times) == 1 else optimal_times

    async def optimal_time_window_and_location(self, locations: List[str], window_len: float, num_options: int = 1, time_range=[0, 47.5]):
        """
        Given a list of locations and a time window, returns the location and start of the time window with lowest
        carbon intensity over the given time range
        :param locations: list of locations, see carbon_api_wrapper.carbon.REGIONS
        :param window_len: number of hours that you wish to optimise for
        :param num_options: define the number of top options returned
        :return: tuple of (location, time), where time is num hours until optimal start time in hh:mm
        """
        costs = []
        for location in locations:
            if self.cache:
                times = self.cache["region_forecast_range"][f"('{location}', 47.5)"]
                # cut upper time range out of cache
                index = int(time_range[1]*2) if time_range[1] < 48 else 95
                times = times[0: index + 1]
            else:
                times = await self.api.region_forecast_range(location, time_range[1])
            # cut off times before min time range
            times = times[int(time_range[0]*2):]
            # convert hours into half hours
            half_hours = int(window_len * 2) if window_len < 48 else 95
            for window in self._window(times, half_hours):
                carbon_cost = sum([f['forecast'] for f in window])
                cost = {'location': location, 'time': window[0]['time'], 'cost': carbon_cost}
                costs.append(cost)
        sorted_options = sorted(costs, key=lambda x: x['cost'])
        optimal_options = sorted_options[0:num_options]
        return optimal_options[0] if len(optimal_options) == 1 else optimal_options
