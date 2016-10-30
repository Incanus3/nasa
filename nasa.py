#!/usr/bin/env python3

from pprint import pprint
from src.utils import flatten, color_print
from src.requests import request

def preprocess_asteroid(asteroid):
  diameter       = asteroid['estimated_diameter']['kilometers']
  close_approach = asteroid['close_approach_data'][0]
  velocity       = close_approach['relative_velocity']['kilometers_per_hour']

  return {'name'                : asteroid['name'],
          # 'url'                 : d['nasa_jpl_url'],
          'magnitude'           : asteroid['absolute_magnitude_h'],
          'hazardous'           : asteroid['is_potentially_hazardous_asteroid'],
          'diameter_min'        : diameter['estimated_diameter_min'],
          'diameter_max'        : diameter['estimated_diameter_max'],
          'velocity'            : velocity,
          'orbiting_body'       : close_approach['orbiting_body'],
          'close_approach_date' : close_approach['close_approach_date'],
          # 'epoch_date'          : close_approach['epoch_date_close_approach'],
          'miss_distance'       : float(close_approach['miss_distance']['kilometers'])}

response     = request('/neo/rest/v1/feed', { 'start_date': '2016-01-01' })
asteroids    = flatten(response['near_earth_objects'].values())
preprocessed = [preprocess_asteroid(asteroid) for asteroid in asteroids]

print(color_print(preprocessed[:5]))

import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
# from mathplotlib import pyplot

df = pd.DataFrame(preprocessed)
# print(df)
# print(df.describe())
# print(df.columns)
# print(df.miss_distance.min())

with PdfPages('figure.pdf') as pdf:
  max_diameters = pd.DataFrame({'diameter_max': df.diameter_max}, columns = ['diameter_max'])
  max_axes      = max_diameters.plot.hist(bins = 100)
  max_figure    = max_axes.get_figure()

  pdf.savefig(max_figure)

  min_diameters = pd.DataFrame({'diameter_min': df.diameter_min}, columns = ['diameter_min'])
  min_axes      = min_diameters.plot.hist(bins = 100)
  min_figure    = min_axes.get_figure()

  pdf.savefig(min_figure)
