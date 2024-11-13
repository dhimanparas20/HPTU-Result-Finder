from flask import Flask, render_template, request, make_response, jsonify
from flask_restful import Api, Resource
from os import system
from module.scraper import filter_data,scrape_all_data


app = Flask(__name__)
api = Api(app)

class Home(Resource):
    def get(self):
        # Render home.html on GET request
        return make_response(render_template('home.html'))

    def post(self):
        # Read the form data sent via POST
        branch = request.form.get('branch')
        semester = request.form.get('semester')
        scheme = request.form.get('scheme')

        all_data = scrape_all_data()
        filtered_data = filter_data(data=all_data,filters=[branch,semester,scheme])
        
        # Return form data as JSON for demonstration
        return make_response(render_template('result.html',data=filtered_data))

# Add the Home resource to the API
api.add_resource(Home, '/')

if __name__ == '__main__':
    app.run(debug=False,threaded=True,port=5000)
    
