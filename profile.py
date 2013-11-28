"""
Profiler for the Rainman Flask App
"""
from werkzeug.contrib.profiler import ProfilerMiddleware
from rainman import app

app.config['PROFILE'] = True
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [50])
app.run(debug = True)