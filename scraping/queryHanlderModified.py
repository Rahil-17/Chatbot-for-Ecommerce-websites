import re
import pymongo
client = pymongo.MongoClient('mongodb://user:password123@ds123963.mlab.com:23963/project', connectTimeoutMS=300000)
db = client.get_default_database()
flipkart_data = db.flipkart_data
def getProductUsingCompare(query):
	if (not "compare" in query) or ("," not in query) or (not query.find("compare") < query.find(",")):
		return []
	query = query[8:].strip()
	productList = [x.strip() for x in query.split(",")]
	print(productList)
	#print(flipkart_data.find_one({"model name":'motor power one'}))
	result = [flipkart_data.find_one({"model name":productList[0]}),flipkart_data.find_one({"model name":productList[1]})]
	return result
def basicQuestion(query):
	m = re.match(r"what (is|are) the (?P<property>\w+) of (?P<product>.*?)[. ?]*$", query)
	try:
		m.groupdict()
	except:
		return []
	y = [m.groupdict()['product'] , m.groupdict()['property']]
	print(y)	
	result = flipkart_data.find_one({"model name":y[0]})
	print(result['audio jack'])
def listAll(query):
	try:
		m = re.match(r"list all (?P<ProductCategory>\w+) with (?P<property>\w+) (?P<compareType>\w+) (?:than\s)*(?P<value>.*?)[. ?]*$",query)
		m.groupdict()
	except:
		return []
	tempDict = {'upto': '<=', 'atmost': '<=', 'atleast': '>=', 'greater': '>', 'less': '<','as':'=='}
	result = flipkart_data.find({})
	#print(result)
	for doc in result:
		val = float(re.sub("\D", "", doc['ram']))
		if eval("%d %s %d"%(val,tempDict[m.groupdict()['compareType']]	,float(m.groupdict()['value'].strip()))):
			print(doc['model name'])
	return [m.groupdict()['property'].strip() , m.groupdict()['value'].strip() ,m.groupdict()['ProductCategory'].strip(), tempDict[m.groupdict()['compareType']] ]
x = "compare redmi note 5 pro, 7a"
#print(x)
#y = getProductUsingCompare(x)
#print(y)
#z = basicQuestion("what is the cost of redmi note 5 pro?")
a = listAll("list all mobiles with ram less than 3.0")
