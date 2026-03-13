from flask import Flask
from pyngrok import ngrok

from routes.auth_routes import auth_bp
from routes.vehicle_routes import vehicle_bp
from routes.staff_routes import staff_bp
from routes.route_routes import route_bp
from routes.income_routes import income_bp
from routes.payroll_routes import payroll_bp
from routes.report_routes import report_bp
from routes.daraja_routes import daraja_bp
from routes.callback_routes import callback_bp
from routes.main_routes import main_bp
from routes.dashboard_routes import dashboard_bp
from flask import render_template

app = Flask(__name__)

app.secret_key = "Sitakihizikazi123"


app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(vehicle_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(route_bp)
app.register_blueprint(income_bp)
app.register_blueprint(payroll_bp)
app.register_blueprint(report_bp)
app.register_blueprint(daraja_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(callback_bp)



@app.route('/')
def dashboard():
    return render_template("dashboard/dashboard.html")


if __name__ == '__main__':
    app.run(debug=True, port=5000)