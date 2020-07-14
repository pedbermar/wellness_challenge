Wellness Challenge
==================

Prerequisites
-------------

- docker and docker-compose

 
Getting Started
---------------

- docker-compose up -d

- Go to http://localhost/load_csv to load csv data from file


HTTP REST framework
-------------------
Pyramid

Endpoints
---------

 - http://localhost/metrics/{metric_type}/{start}/{end}

    - start/end format: YYMMDDhhmmss
    - type:
        - power_avg
        - power_factor_avg
        - energy_avg
        - intensity_avg
        - voltage_avg
        - reactive_power_avg
        - reactive_energy_avg


 - http://localhost/current_month

    returns the metrics average for the current month

 - http://localhost/daily/{type}

    returns daily average of energy (if type is equal to 'energy') or reactive energy (type equal to 'reactive_energy')

 - http://localhost/login?user=default&password=default

    - returns an authentication token for subsecuents API calls (user=default, password = default)
    - Access control to API methods are disable due to lack of time.

Database
--------
- MongoDB

Cache
-----
redis cache (pyramid_beaker)

Authentication
--------------
* jwt tokens (pyramid_jwt)


Technical decisions
-------------------
- URL params for flexibility over have a lot of endpoints
- URL params as path for cleaness
- I choose Pyramid becouse it's a more robust than flask and lightwight than django.
- I choose Mongo becouse is document oriented and has JSON formatted documents, perfect for REST API's
- Mongo becose pipelines are faster than process documents by python code
- JWT becouse it's a standard

Improvements
------------
- API methods access control
- Mongo pipelines sort 
- Test
- Modularity
- Database index (elasticsearch)
