from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/download')
def download_edgebot():
    return render_template('download_edgebot.html')

@bp.route('/wiring-tutorial')
def wiring_tutorial():
    return render_template('wiring_tutorial.html')

@bp.route('/pro-tips')
def pro_tips_page():
    return render_template('pro_tips_page.html')

@bp.route('/docs')
def main_py_documentation():
    return render_template('main_py_documentation.html')

@bp.route('/donate')
def donate():
    return render_template('donate.html')

@bp.route('/control-station')
def control_station():
    return render_template('EdgeBot_MK-II_Control_Station.html') 