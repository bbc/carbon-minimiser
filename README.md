**Carbon Minimisation API**
----
# Background
The National Grid have created [a Carbon Intensity API for the UK](https://api.carbonintensity.org.uk/). This allows for the programmatic access of predictions for carbon intensity across England, Scotland, and Wales.

This information allows you to estimate the optimal time to perform actions to reduce their impact on the planet, by choosing times when your area has a lower carbon intensity.

# What this API does

This API allows you to answer questions like:

```What is the best 4 hour window to charge my electric car in the next 12 hours?```

or

```Which of our UK server locations should I deploy this process to for minimal carbon output?```

# Important Note

You have to host your own version of this API. Feel free to make one publicly available - but remember requests to this API result in multiple requests to the UK Carbon Intensity API, so please use the caching option provided.


## Running the API

### Set up

* Set up a virtual environment:
`python3 -m venv .venv`

* Activate environment:
`source .venv/bin/activate`

* Install dependencies:
`pip install -r requirements.txt`

### Configuration
The default settings are found in `config.ini`. Here you can disable the cache (not recommended), change the cache refresh rate, and change the port number.

It is recommended you edit the LOCATIONS section to only list the locations you expect to be using. This will reduce the time it takes to cache and process your requests.

### Running

To run the API:

`python3 -m carbon_minimiser`

The API will then be available at `http://localhost:8080`

### Testing

To run the suite of tests:

`python3 -m pytest`

## Endpoints

### Optional Parameters
Some calls accept `results` or `range` as optional URL parameters.

#### results
This parameter allows you to return the top `n` results like so:
`?results=5
`
#### range
This parameter allows you to define a timerange you want the results to reside between: `?range=from,to`.

These can be defined in intervals of 0.5 hours from the time of the last cache: `?range=3.5,10`.

The range can be up to 47.5, as this is the furthest away prediction the Carbon Intensity API provides. 

All numbers provided will be clipped to <=47.5, and rounded to the nearest 0.5.


### Returned values

#### time
This is a UTC (+00:00) timestamp in ISO8601 format

#### forecast
This is the forecast amount of CO2 in grams per kWh. For endpoints using a time window this is the averaged cost.

#### index
A measure of the Carbon Intensity represented on a scale between 'very low', 'low', 'moderate', 'high', 'very high'.

#### location
One of the locations defined in config.ini, from the [list of possible locations](https://carbon-intensity.github.io/api-definitions/#region-list)


### Get optimal time and location
#### Returns the place and time over the next 48 hours with the lowest carbon intensity

* **URL:** `/optimise`

* **Method:** `GET`

*  **URL Params**

   **Optional:** `results=[int]`
   **Optional:** `range=[int],[int]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{
      "time": "YYYY-mm-ddThh:mmZ",
      "forecast": int,
      "index": str,
      "location": str
    }`

* **Sample Call:** `curl "http://localhost:8080/optimise?results=2&range=5,10"`

### Get optimal location right now
#### Returns the place with the lowest carbon intensity currently

* **URL:** `/optimise/location`

* **Method:** `GET`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{
      "location": str,
      "cost": int,
      "index": str
    }`

* **Sample Call:** `curl http://localhost:8080/optimise/location`

### Get optimal time for a given location
#### Returns the time over the next 48 hours with the lowest carbon intensity, in the specified location

* **URL:** `/optimise/location/<location>`

* **Method:** `GET`

*  **URL Params**
   
    * **Required:** `<location>` [Key in Regions](https://github.com/bbc/rd-carbon-intensity-exporter/blob/11e17d679f8ff0611d1fd585d493811e603ce3fc/carbon_intensity_exporter/carbon_api_wrapper/carbon.py#L4)
   
    * **Optional:** `results=[int]`
    * **Optional:** `range=[int],[int]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{
      "time": "YYYY-mm-ddThh:mmZ",
      "forecast": int,
      "index": str
    }`
    
* **Error Response:**

  * **Code:** 404 <br />
    **Content:** `"Location not found"`

* **Sample Call:** `curl "http://localhost:8080/optimise/location/n_scotland?results=3&range=0,5"`

### Get optimal time window for a location
#### Given a time window of H hours, returns the optimal start time to minimise average carbon usage over H hours, along with the average carbon forecast in gC02/kWh

* **URL:** `/optimise/location/<location>/window/<window>`

* **Method:** `GET`

*  **URL Params**
   
    * **Required:** 
      * `<location>` [Key in Regions](https://github.com/bbc/rd-carbon-intensity-exporter/blob/11e17d679f8ff0611d1fd585d493811e603ce3fc/carbon_intensity_exporter/carbon_api_wrapper/carbon.py#L4)
      * `<window>` float number of hours (minimum resolution 0.5 hours)  
    * **Optional:** `results=[int]`
    * **Optional:** `range=[int],[int]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{
      "time": "YYYY-mm-ddThh:mmZ",
      "cost": int
    }`
    
* **Error Response:**

  * **Code:** 404 <br />
    **Content:** `"Location not found"`

* **Sample Call:** `curl "http://localhost:8080/optimise/location/n_scotland/window/5?results=3&range=0,5"`

### Get optimal time window and location
#### Given a time window of H hours, returns the optimal start time and location to minimise average carbon over H hours, along with the average carbon forecast in gC02/kWh

* **URL:** `/optimise/location/window/<window>`

* **Method:** `GET`

*  **URL Params**
   
    * **Required:** 
      * `<window>` float number of hours (minimum resolution 0.5 hours)  
    * **Optional:** `results=[int]`
    * **Optional:** `range=[int],[int]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{
      "location": str,
      "time": "YYYY-mm-ddThh:mmZ",
      "cost": int
    }`
    
* **Error Response:**

  * **Code:** 404 <br />
    **Content:** `"Location not found"`

* **Sample Call:** `curl "http://localhost:8080/optimise/location/window/5?results=2&range=0,5"`
