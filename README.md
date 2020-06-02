# Premium Refund Calculator
This calculator accurately calculate the unearned premium based on **SEVEN** input parameters by applying the company reserving method.**SIX** out of **SEVEN** parameters can be found in the database and one required manual input from the end user.

###Table of Contents
<details>
    <summary>click to expand</summary>
    * [Running RESTful API](#running-restful-api)
    	* [Prerequisites](#prerequisites)
    	* [Data format](#data-format)
    	* [Definition of Parameters](#definition-of-parameters)
	* [Running Web Application](#running-Web-application)
</details>

## Running RESTful API
You must have python3.7.4 and above install. Other required packages can be aquired via:<br>
`pip install -r requirements.txt`<br>

To run the service:<br>
`python RESTful_API.py`

### Data format

The service take a json post request and returned the refund amount. The data **must** be in the the following structure:<br>
`{"premium"   : $$$.$$,`<br>
`'issue_date'   : 'yyyy-mm-dd HH:MM:SS',`<br>
`'start_date'   : 'yyyy-mm-dd HH:MM:SS',`<br>
`'end_date'     : 'yyyy-mm-dd HH:MM:SS',`<br>
`'request_date' : 'yyyy-mm-dd HH:MM:SS',`<br>
`'prd_grp_fin'  : 'E-comm',`<br>
`'policy_id'    : 'XXXXX'}`<br>

Example of how to post a request via python is in `request.py`.


### Definition of Parameters:
1. `premium`      - The original GWP/Premmium charged to the policyholders/customers.
2. `issue_date`   - The date when the policy is underwritten.
3. `start_date`   - The initial start date of the trip/journey.
4. `end_date`     - The expiry date of the policy or when the policy become ineffective.
5. `request_date` - The date in which refund begain to take effect from.
6. `prd_grp_fin`  - Segmentation information provided by B.I.
7. `policy_id`    - The identifying id for the request policy. (This is for logging and debugging purpose)


### Running Web Application
`python webapp.py`
