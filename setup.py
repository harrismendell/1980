from dataProject import app
import os
port = int(os.environ.get('PORT', 5000))
print "Port: %s" % port
app.run(debug=True, port=port)