import asyncio
from carbon_api.carbon_api_wrapper.carbon import CarbonAPI, REGIONS
import json

class Cache:
    def __init__(self, refresh_rate):
        self.refresh_rate = refresh_rate
        self.carbonAPI = CarbonAPI()
        self.cache = {}
        self.HOURS_PARAM = 47.5  # Get max forecast
        self.gather_functions()
        asyncio.run(self.periodic_task(refresh_rate, self.create_cache))
    
    async def periodic_task(self, refresh_rate, task):
        await task()  # initial run of task
        while True:
            await asyncio.sleep(refresh_rate)
            await task()  # repeated run of task

    async def create_cache(self):
        self.cache = {}
        for functions in self.functions:
            func = functions['func']
            self.cache[func.__name__] = {}
            params = functions['params']
            print(func.__name__)
            if isinstance(params, list):
                for param in params:
                    print(param)
                    if isinstance(param, tuple):
                        result = await func(*param)
                    else:
                        result = await func(param)
                    self.cache[func.__name__][str(param)] = result
            elif len(params):
                print(param)
                result = await func(*param if isinstance(param, tuple) else param)
                self.cache[func.__name__][params] = result
            else:
                result = await func()
                self.cache[func.__name__] = result
        self.write_cache()

    def write_cache(self):
        with open("cache.json", "w") as f:
            f.write(json.dumps(self.cache))

    def read_cache(self):
        with open("cache.json", "r") as f:
            return json.loads(f.read())

    def gather_functions(self):
        functions_no_params = ["current_national_intensity", "current_national_mix"]
        functions_region_param = ["current_region_intensity", "current_region_mix"]
        functions_hours_param = ["national_forecast_single", "national_forecast_range"]
        functions_region_and_hours_params = ["region_forecast_single", "region_forecast_range"]
        self.functions = []
        for func_name in functions_no_params:
            self.functions.append({"func": getattr(self.carbonAPI, func_name), "params": ""})
        for func_name in functions_region_param:
            self.functions.append({"func": getattr(self.carbonAPI, func_name), "params": [region for region in REGIONS]})
        for func_name in functions_hours_param:
            self.functions.append({"func": getattr(self.carbonAPI, func_name), "params": [self.HOURS_PARAM]})
        for func_name in functions_region_and_hours_params:
            self.functions.append({"func": getattr(self.carbonAPI, func_name), "params": [(region, self.HOURS_PARAM) for region in REGIONS]})
