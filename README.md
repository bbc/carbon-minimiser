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

You have to host your own version of this API. Feel free to make one publically available - but remember requests to this API result in multiple requests to the UK Carbon Intensity API, so please use the caching option provided.


## Running the API

### Set up

* Set up a virtual environment:
`python3 -m venv .venv`

* Activate environment:
`source .venv/bin/activate`

* Install dependencies:
`pip install -r requirements.txt`

### With caching (recommended)
To reduce the demand on the UK Carbon Intensity API, a cache is provided. This updates the cache at 30 minute intervals (the same as the Carbon Intensity API), and vastly increases response times. To run this, run with the `-c` flag:

`python3 carbon_minimiser -c -p 8080`

### Without caching (not recommended)
By disabling the cache the UK Carbon Intensity API will be queried directly on each request. This increases demand on their API and increases latency. To run this option, run without the `-c` flag:

`python3 carbon_minimiser -p 8080`

### Testing

To run the suite of tests:

`python3 -m pytest`
## Endpoints

### Get optimal time and location
#### Returns the place and time over the next 48 hours with the lowest carbon intensity

* **URL:** `/optimise`

* **Method:** `GET`

*  **URL Params**

   **Optional:** `results=[int]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{
      "time": "YYYY-mm-ddThh:mmZ",
      "forecast": int,
      "index": str,
      "location": str
    }`

* **Sample Call:** `curl http://localhost:8080/optimise?results=2`

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

* **Sample Call:** `curl http://localhost:8080/optimise/location/london?results=3`

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
    **Content:** `{
      "time": "YYYY-mm-ddThh:mmZ",
      "cost": int
    }`
    
* **Error Response:**

  * **Code:** 404 <br />
    **Content:** `"Location not found"`

* **Sample Call:** `curl http://localhost:8080/optimise/location/london/window/5?results=3`

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
    **Content:** `{
      "location": str,
      "time": "YYYY-mm-ddThh:mmZ",
      "cost": int
    }`
    
* **Error Response:**

  * **Code:** 404 <br />
    **Content:** `"Location not found"`

* **Sample Call:** `curl http://localhost:8080/optimise/location/window/5?results=2`
