from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.vehicle import Vehicle

garage_bp = Blueprint('garage', __name__, url_prefix='/garage')

@garage_bp.route('/')
def index():
    vehicles = Vehicle.get_all()
    return render_template('garage/index.html', vehicles=vehicles)

@garage_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        brand = request.form.get('brand')
        model_name = request.form.get('model_name')
        current_mileage = request.form.get('current_mileage', type=int)
        
        if not brand or not model_name or current_mileage is None:
            flash('請填寫所有必填欄位', 'danger')
            return render_template('garage/form.html', vehicle=None)
            
        Vehicle.create(brand, model_name, current_mileage)
        flash('車輛已成功新增', 'success')
        return redirect(url_for('garage.index'))
        
    return render_template('garage/form.html', vehicle=None)

@garage_bp.route('/<int:v_id>/edit', methods=['GET', 'POST'])
def edit(v_id):
    vehicle = Vehicle.get_by_id(v_id)
    if not vehicle:
        flash('找不到該車輛', 'danger')
        return redirect(url_for('garage.index'))
        
    if request.method == 'POST':
        brand = request.form.get('brand')
        model_name = request.form.get('model_name')
        current_mileage = request.form.get('current_mileage', type=int)
        
        if not brand or not model_name or current_mileage is None:
            flash('請填寫所有必填欄位', 'danger')
            return render_template('garage/form.html', vehicle=vehicle)
            
        Vehicle.update(v_id, brand, model_name, current_mileage)
        flash('車輛資訊已更新', 'success')
        return redirect(url_for('garage.index'))
        
    return render_template('garage/form.html', vehicle=vehicle)

@garage_bp.route('/<int:v_id>/delete', methods=['POST'])
def delete(v_id):
    Vehicle.delete(v_id)
    flash('車輛已刪除', 'success')
    return redirect(url_for('garage.index'))
