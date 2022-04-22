from asynctest import TestCase, mock
from minimiser_api.minimiser import Minimiser
from carbon_api.carbon_api_wrapper.carbon import CarbonAPI


class TestCarbonMinimiser(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.min = Minimiser()
        cls.min.set_cache(False)

    async def test_optimal_location_now(self):
        data = [(231, 'moderate'), (131, 'moderate'), (331, 'moderate')]
        with mock.patch.object(CarbonAPI, "current_region_intensity", side_effect=data):
            result = await self.min.optimal_location_now(["a", "b", "c"])
            expected_result = {'location': 'b', 'cost': 131, 'index': 'moderate'}
            self.assertEqual(result, expected_result)

    async def test_optimal_time_for_location(self):
        data = [{'forecast': 231, 'index': 'moderate', 'time': '+00:30'},
                {'forecast': 223, 'index': 'moderate', 'time': '+01:00'},
                {'forecast': 218, 'index': 'moderate', 'time': '+01:30'}]
        with mock.patch.object(CarbonAPI, "region_forecast_range", return_value=data):
            result = await self.min.optimal_time_for_location("")
            expected_result = {'forecast': 218, 'index': 'moderate', 'time': '+01:30'}
            self.assertEqual(result, expected_result)

    async def test_optimal_time_and_location(self):
        data = [[{'forecast': 231, 'index': 'moderate', 'time': '+00:30'},
                {'forecast': 23, 'index': 'moderate', 'time': '+01:00'}],
                [{'forecast': 261, 'index': 'moderate', 'time': '+00:30'},
                 {'forecast': 234, 'index': 'moderate', 'time': '+01:00'}],
                [{'forecast': 251, 'index': 'moderate', 'time': '+00:30'},
                 {'forecast': 253, 'index': 'moderate', 'time': '+01:00'}]]
        with mock.patch.object(CarbonAPI, "region_forecast_range", side_effect=data):
            result = await self.min.optimal_time_and_location(["a", "b", "c"])
            expected_result = {'forecast': 23, 'index': 'moderate', 'time': '+01:00', 'location': 'a'}
            self.assertEqual(result, expected_result)

    async def test_optimal_time_window_for_location(self):
        data = [{'forecast': 100, 'index': 'moderate', 'time': '+00:30'},
                {'forecast': 200, 'index': 'moderate', 'time': '+01:00'},
                {'forecast': 50, 'index': 'moderate', 'time': '+01:30'},
                {'forecast': 300, 'index': 'low', 'time': '+02:00'},
                {'forecast': 200, 'index': 'moderate', 'time': '+02:30'},
                {'forecast': 150, 'index': 'moderate', 'time': '+03:00'}]
        with mock.patch.object(CarbonAPI, "region_forecast_range", return_value=data):
            result = await self.min.optimal_time_window_for_location("", 0.5)
            self.assertEqual(result, {'time': "+01:30", 'cost': 50})
            result = await self.min.optimal_time_window_for_location("", 1)
            self.assertEqual(result, {'time': "+01:00", 'cost': 250})
            result = await self.min.optimal_time_window_for_location("", 1.5)
            self.assertEqual(result, {'time': "+00:30", 'cost': 350})
            result = await self.min.optimal_time_window_for_location("", 2)
            self.assertEqual(result, {'time': "+00:30", 'cost': 650})
            result = await self.min.optimal_time_window_for_location("", 2.5)
            self.assertEqual(result, {'time': "+00:30", 'cost': 850})

    async def test_optimal_time_window_and_location(self):
        data = [[{'forecast': 201, 'index': 'moderate', 'time': '+00:30'},
                 {'forecast': 10, 'index': 'moderate', 'time': '+01:00'},
                 {'forecast': 200, 'index': 'moderate', 'time': '+01:30'}],
                [{'forecast': 200, 'index': 'moderate', 'time': '+00:30'},
                 {'forecast': 20, 'index': 'moderate', 'time': '+01:00'},
                 {'forecast': 100, 'index': 'moderate', 'time': '+01:30'}],
                [{'forecast': 200, 'index': 'moderate', 'time': '+00:30'},
                 {'forecast': 250, 'index': 'moderate', 'time': '+01:00'},
                 {'forecast': 200, 'index': 'moderate', 'time': '+01:30'}]]
        with mock.patch.object(CarbonAPI, "region_forecast_range", side_effect=data):
            result = await self.min.optimal_time_window_and_location(["a", "b", "c"], 0.5)
            expected_result = {'location': 'a', 'time': '+01:00', 'cost': 10}
            self.assertEqual(result, expected_result)
        with mock.patch.object(CarbonAPI, "region_forecast_range", side_effect=data):
            result = await self.min.optimal_time_window_and_location(["a", "b", "c"], 1)
            expected_result = {'location': 'b', 'time': '+01:00', 'cost': 120}
            self.assertEqual(result, expected_result)
        with mock.patch.object(CarbonAPI, "region_forecast_range", side_effect=data):
            result = await self.min.optimal_time_window_and_location(["a", "b", "c"], 1.5)
            expected_result = {'location': 'b', 'time': '+00:30', 'cost': 320}
            self.assertEqual(result, expected_result)
