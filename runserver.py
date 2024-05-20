import os
from endoG4 import app

def runserver():
    port = int(os.environ.get('PORT', 5000))
    app.jinja_env.auto_reload = True
    app.run(host='0.0.0.0', port=port, debug=True)
    app.run()

if __name__ == '__main__':
    runserver()