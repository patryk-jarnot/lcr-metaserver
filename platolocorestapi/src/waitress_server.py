from waitress import serve
import src.__main__ as flask_app

serve(flask_app.app, host='0.0.0.0', port=5002)
