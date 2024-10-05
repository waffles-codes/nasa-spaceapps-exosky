wimport ssl
from astroquery.gaia import Gaia
import astropy.units as u
from astropy.coordinates import SkyCoord
from flask import Flask, jsonify, request
import json
import pandas as pd
# ensure you have all dependencies
app = Flask(__name__) #create a flask app

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


# Right ascension (RA) (basically east to west on sphere) and 
# declination (Dec) (basically north south on a sphere)
# are celestial coordinates that specify the position of an object in the sky.
coord = SkyCoord(ra=280, dec=-60, unit=(u.degree, u.degree), frame='icrs')
width = u.Quantity(0.1, u.deg)
height = u.Quantity(0.1, u.deg)
r = Gaia.query_object_async(coordinate=coord, width=width, height=height)
df = r.to_pandas()
json_df = df.to_json()


@app.route('/api/get_coords', methods=['GET'])
def get_coords():
    return json_df

if __name__ == '__main__':
    app.run(port=5000)