import requests, json

gedser = '54.574699,11.92531' 
rodby = '54.660727,11.362782'

key = '7U3pbNM6W5GhxffR1wiRBvdenMFwZZub'

api_str = 'http://www.mapquestapi.com/directions/v2/route?key={0}&locations={1}54.660727,11.362782&unit=k'.format(key, '2000,Denmark')
api_str = 'http://www.mapquestapi.com/directions/v2/routematrix?key={0}'.format(key)

place="2000,Denmark"

body = {
"locations":[
	place,
	gedser,
	rodby
],
"options":
{
	"manyToOne": True,
	"unit": "k"
}
}


r = requests.post(api_str, data=json.dumps(body))

with open("ex.json", 'w+') as outfile:
	json.dump(r.json(), outfile)
