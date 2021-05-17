README
This is a simple API that will create a person object and support CRUD operations using Flask and MongoDB. 
The objects will be saved in the API DB on MongoDB.
The API DB has two collections: person and version.
The person collection will hold the latest version on the object.
The version collection will hold past versions of the object.

This API offers object versioning. 
○ Updates to an existing object will result in a new version of the object being created and update the person collection
○ The old version of an object will be added to the version collection.
○ All versions will be accessible via the API.
○ API will return the newest version of the object by default.
○ Update and Delete actions apply to the latest version of an object.

This API will be posting data to MongoDB and using MongoEngine to handle data.

In order to run this API you will need to install the following libraries:
MongoEngine
Flask
pytest
requests
jsonify

python -m pip install --user pytest Flask requests jsonify MongoEngine

After the libraries have been installed you will need to create an api_constants.py file with the credentials of your DB instance.
The file should look like this:
USER_NAME = "user_name"
MONGODB_PASSWORD = "password"
DATABASE_NAME = "DB_name"

This will populate the MONGO_URI for the config and create a connection to the DB.

After the set you can cd into flask/API and run the server with:
Windows:
py .\person_api.py

Mac:
python person_api.py

Once the server is running you can make API calls using postman or any client available.

Here is a sample call using curl:
GET: get all persons
curl http://127.0.0.1:5000/api/persons

POST:
curl -v --header "Content-Type: application/json" -d "{\"person_id\": 1,\"first_name\":\"Diego\",\"last_name\": \"Ortega\",\"email\": \"test1@test.com\",\"age\": 28}" http://127.0.0.1:5000/api/persons


These are all the API endpoint available:
GET http://127.0.0.1:5000/api/persons

POST http://127.0.0.1:5000/api/persons

GET http://127.0.0.1:5000/api/persons/<person_id>

PUT http://127.0.0.1:5000/api/persons/<person_id>

DELETE http://127.0.0.1:5000/api/persons/<person_id>

GET http://127.0.0.1:5000/api/persons/<person_id>/<version_id>


Run tests by cd into flask/API/tests and run this command:
Windows:
python -m pytest .\person_api_test.py

Mac: 
pytest person_api_test.py

I also used pytest build a report that can be viewed in HTML and that can be created by running:
Windows:
python -m pytest -sv --html report.html

Mac:
pytest -sv --html report.html

This will create a report summary that you view in the report.html in the flask/API directory.