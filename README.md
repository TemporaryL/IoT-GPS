1. IoT GPS Webapp:
   - Flask webapp (including API) for receiving coordinates from device
   - Generates webpages using folium for visualising coordinates using
	    marker(s)
   - Two webpages can be generated with the following paths:
     - /latest
        > Only shows the latest location in the database
     - /map
        > Shows the last 10 locations in the database to plot out last known movements of the device
2. IoT GPS Device:
   - Extracts coordinates from gpspipe, prints to screen, and sends them
	    to the Flask API
3. Installation:
   - Ensure Python 3 and pip are installed (the following are debian based commands which typically uses the aptitude package manager)
     > apt install python3
     
     > apt install python3-pip
   - pip installs:
     > pip install flask
     
     > pip install flask-sqlalchemy
     
     > pip install folium
