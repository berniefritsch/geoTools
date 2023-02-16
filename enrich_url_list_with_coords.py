import sys
import re
import urllib3
import json

http = urllib3.PoolManager()

print(sys.argv[1])

with open(sys.argv[1], 'r') as input_file, open("output.csv", "w") as output_file:

    output_file.write("url,lng,lat\n")
    urls = input_file.readlines()

    for url in urls:
        url = url.strip()
        match = re.match('.*gazetteer.dainst.org/.*/(\d+)', url)

        coords = None

        if match:
            (gaz_id,) = match.groups()
            r = http.request('GET', f'https://gazetteer.dainst.org/doc/{gaz_id}.geojson')
            data = json.loads(r.data)

            if "geometry" in data and "geometries" in data["geometry"]:
                for geometry in data["geometry"]["geometries"]:
                    if geometry["type"] == "Point":
                        coords = geometry["coordinates"]

        if coords is not None:
            output_file.write(f"{url},{coords[0]},{coords[1]}\n")
        else:
            output_file.write(f"{url},unknown,unknown\n")
