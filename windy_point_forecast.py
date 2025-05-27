# Only output the Windy.com map embed code, since API key is not valid for backend requests
iframe_code = '''
<iframe
  width="650"
  height="450"
  src="https://embed.windy.com/embed2.html?lat=50.4&lon=14.3&detailLat=50.4&detailLon=14.3&width=650&height=450&zoom=5&level=surface&overlay=wind&product=ecmwf&menu=&message=true&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"
  frameborder="0"
></iframe>
'''

print(iframe_code)
