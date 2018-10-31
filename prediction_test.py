import json
from circle_predictor import upload_circle

creds = json.load(open('/etc/hackathon/creds.json'))

print(upload_circle(api_url= creds['api_url'],api_key=creds['api_key'],path='/tmp/BitImage_20181030092017_png/circle-46.jpg'))