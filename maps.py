import googlemaps

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
gmaps = googlemaps.Client(key='YOUR_API_KEY')

# Define the coordinates of two locations
origin = "New York, NY"
destination = "Los Angeles, CA"

# Calculate the distance between the two locations
distance_matrix = gmaps.distance_matrix(origin, destination)

# Extract the distance in meters
distance = distance_matrix['rows'][0]['elements'][0]['distance']['value']

print(f"Distance between {origin} and {destination}: {distance} meters")
