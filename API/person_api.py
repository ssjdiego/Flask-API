from flask import Flask, request, jsonify
from flask.helpers import make_response
from flask_mongoengine import MongoEngine
from api_constants import MONGODB_PASSWORD, DATABASE_NAME, USER_NAME


app = Flask(__name__)

DB_URI = "mongodb+srv://{}:{}@cluster0.vt4cl.mongodb.net/{}?retryWrites=true&w=majority".format(
    USER_NAME, MONGODB_PASSWORD, DATABASE_NAME
)
app.config["MONGODB_HOST"] = DB_URI
app.config["MONGO_URI"] = DB_URI

db = MongoEngine()
db.init_app(app)


'''
Sample Request Body
{
    id: 1,
    first_name: "Diego",
    middle_name: "",
    last_name: "Ortega",
    email: "test@test.com",
    age: 28
    version: 1
}
'''
# shema for person object
class Person(db.Document):
    person_id = db.IntField()
    first_name = db.StringField()
    middle_name = db.StringField()
    last_name = db.StringField()
    email = db.StringField()
    age = db.IntField()
    version = db.IntField()
    
    def to_json(self):
        # converts this document to JSON
        return {
            "person_id": self.person_id, 
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "age": self.age,
            "version": self.version
        }

# schema for object version
class Version(db.Document):
    person_id = db.IntField()
    first_name = db.StringField()
    middle_name = db.StringField()
    last_name = db.StringField()
    email = db.StringField()
    age = db.IntField()
    version = db.IntField()
    
    def to_json(self):
        # converts this document to JSON
        return {
            "person_id": self.person_id, 
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "age": self.age,
            "version": self.version
        }

'''
GET /api/persons Fetch a list of all persons (latest version) (200 success)

POST /api/persons Create a new person (201 success)

GET /api/persons/1 Fetch the latest version of a single person using their id (200 sucess)

PUT /api/persons/1 Update a single person using their id (204 success)

DELETE /api/persons/1 Delete a single person using their id (204 success)
 
GET /api/persons/1/v1 Fetch a single person using their id and a specified version (200 success)
'''

# this is a test endpoint to create some test data
@app.route('/api/db_populate', methods=['POST'])
def db_populate():
    person1 = Person(person_id = 1, first_name = "Diego", middle_name = "", last_name = "Ortega", email = "test1@test.com", age = 28, version = 1)
    person2 = Person(person_id = 2, first_name = "John", middle_name = "", last_name = "Smith", email = "test2@test.com", age = 29, version = 1)
    person1.save()
    person2.save()
    return make_response("", 201)

@app.route('/api/persons', methods=['GET','POST'])
def api_persons():
    if request.method == 'GET':
        persons = []
        for person in Person.objects:
            persons.append(person)
        return make_response(jsonify(persons), 200)
    
    elif request.method == 'POST':
        data = request.json
        request_id = data.get("person_id", None)
        request_first_name = data.get("first_name", None)
        request_middle_name = data.get("middle_name", None)
        request_last_name = data.get("last_name", None)
        request_email = data.get("email", None)
        request_age = data.get("age", None)

        if request_id and request_first_name and request_last_name and request_email and request_age:
            person_obj = Person.objects(person_id = request_id).first()
            if person_obj:
                message = {
                    'message': "Duplicate person with same id: " + str(request_id),
                    'request_url': request.url,
                    'status': 404
                }
                response = jsonify(message)
                return make_response(response, 404)
            else:
                person = Person(   person_id = request_id, 
                                    first_name = request_first_name, 
                                    middle_name = request_middle_name, 
                                    last_name = request_last_name, 
                                    email = request_email, 
                                    age = request_age,
                                    version = 1
                                )
                person.save()
                message = {
                    'message': "Person created",
                    'id': request_id,
                    'request_url': request.url,
                    'status': 201
                }
                response = jsonify(message)
                return make_response(response, 201)
        else:
            return not_found()

@app.route('/api/persons/<id>', methods=['GET','PUT','DELETE'])
def api_each_person(id):
    if request.method == 'GET':
        person_obj = Person.objects(person_id = id).first()
        if person_obj:
            return make_response(jsonify(person_obj), 200)
        else:
            return not_found
    
    elif request.method == 'PUT':
        data = request.json
        person_obj = Person.objects(person_id = id).first()
        if person_obj:
            oldVersion = Version(   person_id = person_obj.person_id, 
                                    first_name = person_obj.first_name, 
                                    middle_name = person_obj.middle_name, 
                                    last_name = person_obj.last_name, 
                                    email = person_obj.email,
                                    age = person_obj.age,
                                    version = person_obj.version
                                )
            oldVersion.save()
            
            request_first_name = data.get("first_name", person_obj.first_name)
            request_middle_name = data.get("middle_name", person_obj.middle_name)
            request_last_name = data.get("last_name", person_obj.last_name)
            request_email = data.get("email", person_obj.email)
            request_age = data.get("age", person_obj.age)
            
            person_obj.update(  person_id = id, 
                                first_name = request_first_name, 
                                middle_name = request_middle_name,
                                last_name = request_last_name,
                                email = request_email,
                                age = request_age,
                                version = person_obj.version + 1
                            )
            message = {
                'message': "Person updated",
                'id': id,
                'request_url': request.url,
                'status': 200
            }
            response = jsonify(message)
            return make_response(response, 200)
        else:
            return not_found()

    elif request.method == 'DELETE':
        person_obj = Person.objects(person_id = id).first()
        if person_obj:
            person_obj.delete()
            message = {
                'message': "Person deleted",
                'id': id,
                'request_url': request.url,
                'status': 200
            }
            response = jsonify(message)
            # delete all versions of person
            # for person in Version.objects(person_id = id):
            #     person.delete()
            return make_response(response, 200)
        else:
            return not_found()

@app.route('/api/persons/<id>/<version_id>', methods=['GET'])
def api_each_person_version(id, version_id):
    person_obj = Person.objects(person_id = id, version = version_id).first()
    if person_obj:
        return make_response(jsonify(person_obj), 200)
    else:
        person_obj = Version.objects(person_id = id, version = version_id).first()
        if person_obj:
            return make_response(jsonify(person_obj), 200)
        else:
            return not_found()

def not_found():
    message = {
        'message': 'Resource Not Found',
        'request_url': request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


    

if __name__ == '__main__':
    app.run()