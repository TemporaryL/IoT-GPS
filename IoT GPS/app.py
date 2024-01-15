from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json, folium

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///O:/Documents/Scripts ~ Tidbits/Python/Flask Websites/IoT GPS/coordinate_log.db'
db = SQLAlchemy(app)

class Coordinates(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	latitude = db.Column(db.Float)
	longitude = db.Column(db.Float)
	timestamp = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

# Custom marker icon
icon_image = "Flask Websites\IoT GPS\static\marker-icon.png"
icon = folium.CustomIcon(
	icon_image,
	icon_size=(25, 41),
	icon_anchor=(12.5, 41))

# Define the default map
default_map = folium.Map(location=[51.5074, -0.1278], zoom_start=7)

# Route to serve the favicon.ico file
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Route to redirect the root URL to the main map page
@app.route('/')
def redirect_from_root():
    return redirect(url_for('show_map'))

@app.route('/receive_location', methods=['POST'])
def receive_location():
	try:
		data = request.get_json()
		latitude = data['lat']
		longitude = data['lon']
		print("Received coordinates:", latitude, longitude)

		new_location = Coordinates(latitude=data['lat'], longitude=data['lon'])
		db.session.add(new_location)
		db.session.commit()
		return jsonify({'message': 'Coordinates logged to database'}), 201
	except Exception as e:
		return jsonify({'error': str(e)}), 400

@app.route('/latest')
def latest_location():
	# global icon
	last_location = Coordinates.query.order_by(Coordinates.timestamp.desc()).first()
	# Add a marker for the latest location
	if last_location:
		# Extract latitude and longitude
		lat, lon = last_location.latitude, last_location.longitude
		# Center Folium map on the latest location
		latest_map = folium.Map(location=[lat, lon], zoom_start=18)
		# Customize the popup content and size
		popup_content = f'Timestamp: {last_location.timestamp}'
		popup = folium.Popup(popup_content, max_width=300) # Adjust max_width as needed
		folium.Marker(location=[lat, lon], icon=icon, popup=popup).add_to(latest_map)
	# Generate the webpage for the latest location
	try:
		return latest_map._repr_html_()
	except:
		return default_map._repr_html_()

@app.route('/map')
def show_map():
	# Query the last 10 rows from the database
	last_10_locations = Coordinates.query.order_by(Coordinates.timestamp.desc()).limit(10).all()
	last_10_map = folium.Map()
	# Proceed if there are 10 locations
	if last_10_locations:
		# Create a Folium map
		last_10_map = folium.Map(location=[last_10_locations[0].latitude, last_10_locations[0].longitude], zoom_start=18)
		# Add markers for the last 10 locations
		for location in last_10_locations:
			# print(location.latitude, location.longitude)
			# Set the popup content to be the timestamp for when the location was seen by the API
			popup_content = f'Timestamp: {location.timestamp}'
			# Create the popup with a width to allow for the timestamp popup content
			popup = folium.Popup(popup_content, max_width=300)
			# Extract latitude and longitude
			lat, lon = location.latitude, location.longitude
			# Create the marker
			folium.Marker(location=[lat, lon], icon=icon, popup=popup).add_to(last_10_map)
	# Generate the webpage for the last 10 locations
	try:
		return last_10_map._repr_html_()
	except:
		return default_map._repr_html_()

if __name__ == '__main__':
	with app.app_context():
		db.create_all()
	app.run(host='192.168.0.10', port=80, debug=True)