import json
import http
import decimal
import sys
import tempfile
from flask import *

from flask_cors import CORS
from io import BytesIO
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
from MPAPI_GPX_classes import *

#use this to return the JSON string to the screen
def get_JSON(item):
	return app.response_class(json.dumps(item,cls=DecimalEncoder), content_type='application/json')

app = Flask(__name__)
#cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = b'_5#ydhhL"F4Qewaxec]/'
mpapi_gpx = MPAPI_GPX()

@app.route('/', methods=['GET', 'POST'])
def show_login():
	 
	if request.method == 'POST':       
		try:	
			profile = mpapi_gpx.getMP_Profile(request.form['username'])		
			flash("Found Profile for " + profile['name']+ "!")
			return render_template('main.html', username=request.form['username'],profile=profile)
		except(http.client.InvalidURL) as error:
			return render_template('main.html',error=error)
	else:
		return render_template('main.html')

@app.route('/downloads/<string:username>', methods=['GET', 'POST'])
def download(username):
	output = mpapi_gpx.getMP_GPX(username)
	resp = make_response(output)
	resp.headers['Content-Type'] = 'text/xml;charset=UTF-8'
	resp.headers['Content-Disposition'] = 'attachment;filename=todos.gpx'
	return resp
	
@app.errorhandler(403)
def page_not_found(error):
	error = "Wrong username or password."
	return render_template('main.html', error=error)

@app.errorhandler(500)
def catch_all(error):
	error = "Well that didn't seem to work."
	return render_template('main.html', error=error)

if __name__ == '__main__':
	app.run()