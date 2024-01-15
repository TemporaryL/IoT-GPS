import subprocess, json, time, select, requests

command = ["gpspipe", "-w"]
process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True, shell=False, bufsize=1, universal_newlines=True)

# Send latitude and longitude to Flask API
api_url = "http://167.99.145.159:5000/receive_location"

while process.poll() is None:
	readable, _, _ = select.select([process.stdout], [], [], 1.0)
	if readable:
		line = process.stdout.readline()
		if line:
			try:
				line = json.loads(line)
				lat = line.get("lat")
				lon = line.get("lon")
				if "lat" in line and "lon" in line:
					if len(str(lat).split('.')[-1]) > 2 and len(str(lon).split('.')[-1]) > 2:
						print(f"{lat}, {lon}")
						try:
							payload = {'lat': lat, 'lon': lon}
							response = requests.post(api_url, json=payload)
							if response.status_code == 200:
								#print("Location sent successfully to Flask API")
								continue
							else:
								print("Failed to send location. Response:", response.text)
								continue
						except Exception as e:
							print("Error:", str(e))
							continue
			except json.JSONDecodeError as e:
				print(f"Error decoding JSON: {e}")
		time.sleep(5)
