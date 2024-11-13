from flask import Flask, render_template, request, make_response, jsonify,Response
from flask_restful import Api, Resource
from os import system
from module.scraper import filter_data,scrape_all_data,extract_id_from_url,fetch_result_by_rollNo

app = Flask(__name__)
api = Api(app)

#Render the Home Screen
class Home(Resource):
    def get(self):
        # Render home.html on GET request
        return make_response(render_template('home.html'))

#Render the Results
class Result(Resource):
    def get(self):
        # Read the form data sent via POST
        branch = request.args.get('branch')
        semester = request.args.get('semester')
        scheme = request.args.get('scheme')
        
        filters = [branch,semester,scheme,'B.TECH']
        all_data = scrape_all_data()
        filtered_data = filter_data(data=all_data,filters=filters)
        
        # Return form data as JSON for demonstration
        return make_response(render_template('result.html',data=filtered_data))

    def post(self):
        # Get data from the POST request
        roll_no = request.form.get('rollNo')
        result_url = request.form.get('result_url')

        # Extract specific ID from result URL
        specific_id = extract_id_from_url(url=result_url)

        if not roll_no:
            return jsonify({"error": "Please provide Roll Number."}), 400
        
        html_content = fetch_result_by_rollNo(rollNo=roll_no, id=specific_id)

        # Return the HTML content directly to the frontend
        return Response(html_content, mimetype='text/html')
  
# Add the Home resource to the API
api.add_resource(Home, '/')
api.add_resource(Result, '/result')

if __name__ == '__main__':
    app.run(debug=False,threaded=True,port=5000) 
