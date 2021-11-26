**Carbon Minimisation API**
----
This API provides a series of optimisation functions against the UK Carbon Intensity API.

This allows you to decide the best time and location to run electricity-intensive operations.

It currently only optimises across London and Manchester ("NW_ENGLAND" to the API) - but this can easily be expanded by extending [this](https://github.com/bbc/rd-carbon-intensity-exporter/blob/58da00a3428171b5cfd020044c5f378faa3ff2a4/carbon_minimiser/api/app.py#L8) list.
### Get optimal time and location
#### Returns the place and time over the next 48 hours with the lowest carbon intensity

* **URL:** `/optimise`

* **Method:** `GET`

*  **URL Params**

   **Optional:** `results=[int]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[[location, +hh:mm], [location, +hh:mm]]`

* **Sample Call:** `curl http://test.mist.rd.bbc.co.uk:8000/optimise?results=2`

### Get optimal location right now
#### Returns the place with the lowest carbon intensity currently

* **URL:** `/optimise/location`

* **Method:** `GET`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `location`

* **Sample Call:** `curl http://test.mist.rd.bbc.co.uk:8000/optimise/location`

### Get optimal time for a given location
#### Returns the time over the next 48 hours with the lowest carbon intensity, in the specified location

* **URL:** `/optimise/location/<location>`

* **Method:** `GET`

*  **URL Params**
   
    * **Required:** `<location>` [Key in Regions](https://github.com/bbc/rd-carbon-intensity-exporter/blob/11e17d679f8ff0611d1fd585d493811e603ce3fc/carbon_intensity_exporter/carbon_api_wrapper/carbon.py#L4)
   
    * **Optional:** `results=[int]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[+hh:mm, +hh:mm, +hh:mm]`
    
* **Error Response:**

  * **Code:** 404 <br />
    **Content:** `"Location not found"`

* **Sample Call:** `curl http://test.mist.rd.bbc.co.uk:8000/optimise/location/london?results=3`

### Get optimal time window for a location
#### Given a time window of H hours, returns the optimal start time to minimise carbon usage over H hours

* **URL:** `/optimise/location/<location>/window/<window>`

* **Method:** `GET`

*  **URL Params**
   
    * **Required:** 
      * `<location>` [Key in Regions](https://github.com/bbc/rd-carbon-intensity-exporter/blob/11e17d679f8ff0611d1fd585d493811e603ce3fc/carbon_intensity_exporter/carbon_api_wrapper/carbon.py#L4)
      * `<window>` float number of hours (minimum resolution 0.5 hours)  
    * **Optional:** `results=[int]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[+hh:mm, +hh:mm, +hh:mm]`
    
* **Error Response:**

  * **Code:** 404 <br />
    **Content:** `"Location not found"`

* **Sample Call:** `curl http://test.mist.rd.bbc.co.uk:8000/optimise/location/london/window/5?results=3`

### Get optimal time window and location
#### Given a time window of H hours, returns the optimal start time and location to minimise carbon over H hours

* **URL:** `/optimise/location/window/<window>`

* **Method:** `GET`

*  **URL Params**
   
    * **Required:** 
      * `<window>` float number of hours (minimum resolution 0.5 hours)  
    * **Optional:** `results=[int]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[[location, +hh:mm], [location, +hh:mm]]`
    
* **Error Response:**

  * **Code:** 404 <br />
    **Content:** `"Location not found"`

* **Sample Call:** `curl http://test.mist.rd.bbc.co.uk:8000/optimise/location/window/5?results=2`
