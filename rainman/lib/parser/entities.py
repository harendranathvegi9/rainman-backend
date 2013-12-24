"""
Classes representing each type of Named Entity.
"""

class Entity(object):
	def __init__(self, entity):
		"""
		Python object representing Named Entity.
		"""
		# original text match
		self.text = entity['text']
		# type of entity
		self.type = entity['type']
		# relevance score
		self.relevance = float(entity['relevance'])
		# count in article
		self.count = int(entity['count'])

		# info for disambiguity
		try:
			self.disambiguated = entity['disambiguated']
		except:
			pass
		# list of indice tuples
		# self.indices

	def fetch_info(self):
		"""
		Method to fetch info from external service.
		"""
		pass

	def output(self):
		"""
		Default output returns just Named Entity name & type.
		"""
		return {
			'text': self.text,
			'type': self.type
		}

	def verbose(self):
		"""
		Verbose output returns extra information for admin view.
		"""
		return {
			'text': self.text,
			'type': self.type,
			'relevance': self.relevance,
			'count': self.count
		}