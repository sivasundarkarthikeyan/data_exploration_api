Folder Contents:
|   app.yaml - Required for GCP deployment
|   data.csv - The data source which is explored using this API
|   main.py - Flask API endpoint script
|   README.md -  Contains information about other files and folders in this directory
|   requirements.txt - List of all necessary packages for the solution to work
|   Stats.py - Python class which acts as an interface between Flask API endpoint and the data
|
\---static - Folder with static elements
        swagger.yaml - Swagger UI for exploring and testing the API


Installation:
	1. Clone the repository 
	2. The solution was created using Python 3.9.0.
	3. Use requirements.txt to install the necessary packages.
		pip install -r requirements.txt
	4. While testing the solution locally, /upload endpoint will work only Linux as storage location is Linux specific (/tmp).


General Information:
	1. https://mcmakler-challenge.ey.r.appspot.com/swagger/ is the link for exploring and testing the API.
	2. The endpoints are secured using basic authentication. Use the below credentials to avoid STATUS_CODE 401 while exploring the API.
		USERNAME:luffy
		PASSWORD:Qn94vt--aeNHKK7
	3. The argument "filename" is optional for all the endpoints. This is provided to allow similar data exploration on the files uploaded using the endpoint /upload. If the new file needs to be explored, provide the name of the uploaded file as value for "filename" argument.
	4. Swagger UI has dummy data in the preview and will result in unfavourable response. Find below the sample request data for each endpoint to test the API.
	5. Feel free to test the API with different values but it is necessary to use the exact keynames for the dictionaries/objects to avoid STATUS_CODE 204 or 500.


Sample Request Data:	
1. /get/stats

• For total unique values
{
    "filename": "data.csv",
    "column": "MSZoning",
    "method": "values"
}

• For most frequent item, this returns a list as there may be more than one frequent item
{
    "filename": "data.csv",
    "column": "MSZoning",
    "method": "common"
}

	
2. /get/top-n
	
{
    "filename": "data.csv",
    "filters": {
        "column": [
            "MSZoning",
            "LotArea",
            "YrSold"
        ],
        "order": [
            true,
            false,
            false
        ],
        "limit": 6
    }
}
	

3. /filter/data, /filter/matches, and /filter/matches-data (These 3 endpoints use the same data format)

{
    "filename": "data.csv",
    "filters": [
        {
            "column": "MSZoning",
            "operator": "eq",
            "value": "RL"
        },
        {
            "column": "LotArea",
            "operator": "leq",
            "value": 10000
        },
        {
            "column": "YrSold",
            "operator": "geq",
            "value": 50
        },
        {
            "column": "Neighborhood",
            "operator": "neq",
            "value": "CollgCr"
        }
    ]
}
	

4. /filter/by-name

{
    "filename": "data.csv",
    "filters": [
        {
            "column": "BldgType",
            "value": "Fam"
        },
        {
            "column": "HouseStyle",
            "value": "Story"
        },
        {
            "column": "Electrical",
            "value": "Fuse"
        }
    ]
}
	
5. /filter/by-id
	
{
    "filename": "data.csv",
    "ids": [
        1,
        2,
        3,
        4
    ]
}
