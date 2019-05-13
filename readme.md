# Item Catalog

## Description

This is an Item catalog where you can create catagories, then add items to each catagory.

## Getting Started

### dependenices:

* python==3.6.7
* Flask==1.0.2
* SQLAlchemy==1.3.2
* psycopg2==2.8.1
* Flask-SQLAlchemy==2.4.0
* Flask-WTF==0.14.2

## Authentication

To use this application you will need to go to https://console.developers.google.com
* create an OAuth 2.0 client id.
* setup the redirect urls and authorized javascript origins
```JSON
"redirect_uris": [
    "http://localhost:5000/",
    "http://localhost:5000/login",
    "http://localhost:5000/gconnect"
],
"javascript_origins": [
    "http://localhost:5000"
] 
```
* then you will need to download json from the google page, rename it to client_secrets.json and place it at the root of this project.
* open the login.html and replace the client_id with the one of the you generated.

## Usage
3. Navigate to the directory [run.py](./run.py) is in.
4. Execute python3 [run.py](./run.py).
5. navigate to localhost:5000

## JSON endpoints

* /catagories/JSON
* /catagories/items/JSON
* /catagories/<int:catagory_id>/items/JSON

## Credits

login.html auth javascript is credited to [Shyam G.](https://gist.github.com/shyamgupta/d8ba035403e8165510585b805cf64ee6)

# License
Logs Analysis is released under the [MIT License](https://opensource.org/licenses/MIT).