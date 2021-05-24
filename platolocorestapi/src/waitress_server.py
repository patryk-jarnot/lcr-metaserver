from waitress import serve
import platolocorestapi.src.__main__ as flask_app

serve(flask_app.app, host='0.0.0.0', port=5002)
# serve(flask_app.app, host='127.0.0.1', port=5002)
