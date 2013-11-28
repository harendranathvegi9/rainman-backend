from nose.tools import eq_
import rainman

class TestAPI:

	def setUp(self):
		rainman.app.config['TESTING'] = True
		self.app = rainman.app.test_client()

	def tearDown(self):
		return

	def test_crossdomain(self):
		response = self.app.get('/api/article')
		eq_(response.status_code, 405)