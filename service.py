from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import psycopg2

app = Flask(__name__)
api = Api(app)

class Timezone(Resource):
    """
    calculate timezone of coordinate
    a point is always in an area, here it is a timezone-polygon
    """
    #set default
    user = 'mohi'
    host = 'localhost'
    dbname = 'timezone'
    password = ''
    
    def __init__(self,dbname=dbname,user=user,host=host,password=password):
    	'''
    	set databasename, user, host and password
    	'''
    	self.dbname = dbname
    	self.user = user
    	self.host = host
    	self.password = password
    	Resource.__init__(self)
    
    def get_timezone(self, point):
		'''
		query database and intersect
		'''
		query = 'SELECT tzid FROM timezone WHERE ST_Intersects(geom, ST_SetSRID(ST_MakePoint(%s, %s),4326))'
		connstr = "dbname='%s' user='%s' host='%s'"
		passstr = " password='%s'"
		
		try:
			connstr = connstr % (self.dbname, self.user, self.host)
			if self.password != '':
				connstr = connstr + passstr % self.password
			conn = psycopg2.connect("dbname='timezone' user='mohi' host='localhost'")
		except:
			return 'connection failed'
		
		cur = conn.cursor()
		try:
			cur.execute(query % (point['lon'],point['lat']))
		except:
			return 'query failed'
		
		rows = cur.fetchall()
		for row in rows:
			return row[0]
	
    def get_timezones(self):
		'''
		query database and return all timezones
		'''
		query = 'SELECT distinct tzid FROM timezone ORDER BY tzid ASC'
		connstr = "dbname='%s' user='%s' host='%s'"
		passstr = " password='%s'"
		
		try:
			connstr = connstr % (self.dbname, self.user, self.host)
			if self.password != '':
				connstr = connstr + passstr % self.password
			conn = psycopg2.connect("dbname='timezone' user='mohi' host='localhost'")
		except:
			return 'connection failed'
		
		cur = conn.cursor()
		try:
			cur.execute(query)
		except:
			return 'query failed'
		
		rows = cur.fetchall()
		#cleaning up
		ret_array = []
		for row in rows:
			ret_array.append(row[0])
		return ret_array

    def get(self):
    	'''
    	parse the parameters
    	then query to database
    	intersect the point and the mulipolygons
    	'''
    	parser = reqparse.RequestParser()
    	parser.add_argument('lat',type=str)
    	parser.add_argument('lon',type=str)
    	point = parser.parse_args()
    	if not point['lat']:
    		return self.get_timezones()
    	else:
    		return self.get_timezone(point)
	

api.add_resource(Timezone, '/timezones')

if __name__ == '__main__':
    app.run(debug=True)