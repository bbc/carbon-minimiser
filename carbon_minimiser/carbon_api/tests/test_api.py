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
from asynctest import TestCase, mock
from carbon_minimiser.carbon_api.carbon_api_wrapper.carbon import CarbonAPI
from carbon_minimiser.carbon_api.carbon_api_wrapper.api_connection import ApiConnection


class TestCarbonAPI(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.carbon = CarbonAPI()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    async def test_current_national_intensity(self):
        data = {'data': [{'intensity': {'actual': 170, 'index': 'moderate'}}]}
        with mock.patch.object(ApiConnection, "get", return_value=data):
            result = await self.carbon.current_national_intensity()
            self.assertEqual(result, (170, 'moderate'))

    async def test_current_region_intensity(self):
        data = {'data': [{'data': [{'intensity': {'forecast': 170, 'index': 'moderate'}}]}]}
        with mock.patch.object(ApiConnection, "get", return_value=data):
            result = await self.carbon.current_region_intensity("LONDON")
            self.assertEqual(result, (170, 'moderate'))

    async def test_current_national_mix(self):
        data = {'data': {'generationmix': [{"fuel": "biomass", "perc": 3.6}, {"fuel": "coal", "perc": 0.4}]}}
        with mock.patch.object(ApiConnection, "get", return_value=data):
            result = await self.carbon.current_national_mix()
            self.assertEqual(result, {'biomass': 3.6, 'coal': 0.4})

    async def test_current_region_mix(self):
        data = {'data': [{'data': [{'generationmix': [{"fuel": "biomass", "perc": 3.6}, {"fuel": "coal", "perc": 0.4}]}]}]}
        with mock.patch.object(ApiConnection, "get", return_value=data):
            result = await self.carbon.current_region_mix("LONDON")
            self.assertEqual(result, {'biomass': 3.6, 'coal': 0.4})

    async def test_national_forecast_single(self):
        data = {'data': [{'intensity': {'forecast': 233, 'index': 'moderate'}},
                         {'intensity': {'forecast': 231, 'index': 'moderate'}},
                         {'intensity': {'forecast': 223, 'index': 'moderate'}},
                         {'intensity': {'forecast': 218, 'index': 'moderate'}},
                         {'intensity': {'forecast': 211, 'index': 'moderate'}},
                         {'intensity': {'forecast': 214, 'index': 'moderate'}}]}
        with mock.patch.object(ApiConnection, "get", return_value=data):
            result = await self.carbon.national_forecast_single(1.5)
            self.assertEqual(result, (218, 'moderate'))

    async def test_national_forecast_range(self):
        data = {'data': [{'from': '2021-04-27T08:30Z', 'intensity': {'forecast': 233, 'index': 'moderate'}},
                         {'from': '2021-04-27T09:00Z', 'intensity': {'forecast': 231, 'index': 'moderate'}},
                         {'from': '2021-04-27T09:30Z', 'intensity': {'forecast': 223, 'index': 'moderate'}},
                         {'from': '2021-04-27T10:00Z', 'intensity': {'forecast': 218, 'index': 'moderate'}},
                         {'from': '2021-04-27T10:30Z', 'intensity': {'forecast': 218, 'index': 'moderate'}},
                         {'from': '2021-04-27T11:00Z', 'intensity': {'forecast': 214, 'index': 'moderate'}}]}
        with mock.patch.object(ApiConnection, "get", return_value=data):
            result = await self.carbon.national_forecast_range(1.5)
            expected = [{'time': '2021-04-27T08:30Z', 'forecast': 233, 'index': 'moderate'},
                        {'time': '2021-04-27T09:00Z', 'forecast': 231, 'index': 'moderate'},
                        {'time': '2021-04-27T09:30Z', 'forecast': 223, 'index': 'moderate'},
                        {'time': '2021-04-27T10:00Z', 'forecast': 218, 'index': 'moderate'}]
            self.assertEqual(result, expected)

    async def test_region_forecast_single(self):
        data = {'data': {'data': [{'intensity': {'forecast': 233, 'index': 'moderate'}},
                                  {'intensity': {'forecast': 231, 'index': 'moderate'}},
                                  {'intensity': {'forecast': 223, 'index': 'moderate'}},
                                  {'intensity': {'forecast': 218, 'index': 'moderate'}},
                                  {'intensity': {'forecast': 218, 'index': 'moderate'}},
                                  {'intensity': {'forecast': 214, 'index': 'moderate'}}]}}
        with mock.patch.object(ApiConnection, "get", return_value=data):
            result = await self.carbon.region_forecast_single(region="LONDON", hours=1.5)
            self.assertEqual(result, (218, 'moderate'))

    async def test_region_forecast_range(self):
        data = {'data': {'data': [{'from': '2021-04-27T08:30Z', 'intensity': {'forecast': 233, 'index': 'moderate'}},
                                  {'from': '2021-04-27T09:00Z', 'intensity': {'forecast': 231, 'index': 'moderate'}},
                                  {'from': '2021-04-27T09:30Z', 'intensity': {'forecast': 223, 'index': 'moderate'}},
                                  {'from': '2021-04-27T10:00Z', 'intensity': {'forecast': 218, 'index': 'moderate'}},
                                  {'from': '2021-04-27T10:30Z', 'intensity': {'forecast': 218, 'index': 'moderate'}},
                                  {'from': '2021-04-27T11:00Z', 'intensity': {'forecast': 214, 'index': 'moderate'}}]}}
        with mock.patch.object(ApiConnection, "get", return_value=data):
            result = await self.carbon.region_forecast_range(region="LONDON", hours=1.5)
            expected = [{'time': '2021-04-27T08:30Z', 'forecast': 233, 'index': 'moderate'},
                        {'time': '2021-04-27T09:00Z', 'forecast': 231, 'index': 'moderate'},
                        {'time': '2021-04-27T09:30Z', 'forecast': 223, 'index': 'moderate'},
                        {'time': '2021-04-27T10:00Z', 'forecast': 218, 'index': 'moderate'}]
            self.assertEqual(result, expected)
