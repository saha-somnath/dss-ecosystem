import dss
import os

access_key = "minioadmin"
access_secret = "minioadmin"
#discover_endpoint = 'http://127.0.0.1:9001'
discover_endpoint = 'http://localhost6:9001'

def main():
	# Provide non-default options
	option = dss.clientOption();
	option.maxConnections = 1;

	# Create a client session against minio cluster(s)
	# It could fail b/c:
	#	1) network unreachable	
	#	2) config file 'conf.json' or containing bucket 'bss' is missing
	try:
		client = dss.createClient(discover_endpoint, access_key,
								  access_secret, option)
	except Exception as e:
		print(e)
		return None

	# Upload this script to cluster under key name exampleXX
	key_base = 'example'
	filename = os.path.abspath(__file__)
	for i in range(20):
		key = key_base + str(i)
		client.putObject(key, filename)

	# Print objects with prefix
	objects = client.getObjects(key_base, '/')
	while True:
		try:
			it = iter(objects)
		except dss.NoIterator:
			break
		while True:
			try:
				key = next(it)
				print("{}".format(key))
			except StopIteration:
				break

	# Retrieve object then delete
	for i in range(20):
		key = key_base + str(i)
		try:
			client.getObject(key, '/tmp/' + key)
		except Exception as e:
			print(e)
			return None

		client.deleteObject(key)

if __name__ == "__main__":
	main()
