from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.vehicle import Vehicle
from app.models.maintenance import MaintenanceRecord

maintenance_bp = Blueprint('maintenance', __name__)

@maintenance_bp.route('/garage/<int:v_id>/maintenance/')
def index(v_id):
    vehicle = Vehicle.get_by_id(v_id)
    if not vehicle:
        flash('找不到該車輛', 'danger')
        return redirect(url_for('garage.index'))
        
    records = MaintenanceRecord.get_by_vehicle(v_id)
    return render_template('maintenance/index.html', vehicle=vehicle, records=records)

@maintenance_bp.route('/garage/<int:v_id>/maintenance/add', methods=['GET', 'POST'])
def add(v_id):
    vehicle = Vehicle.get_by_id(v_id)
    if not vehicle:
        return redirect(url_for('garage.index'))
        
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        mileage_at_service = request.form.get('mileage_at_service', type=int)
        interval_mileage = request.form.get('interval_mileage', type=int)
        cost = request.form.get('cost', type=int, default=0)
        service_date = request.form.get('service_date')
        notes = request.form.get('notes', '')
        
        if not item_name or mileage_at_service is None or not service_date:
            flash('請填寫必填欄位（項目、里程、日期）', 'danger')
            return render_template('maintenance/form.html', vehicle=vehicle, record=None)
            
        MaintenanceRecord.create(v_id, item_name, mileage_at_service, interval_mileage, cost, service_date, notes)
        flash('保養紀錄已新增', 'success')
        return redirect(url_for('maintenance.index', v_id=v_id))
        
    return render_template('maintenance/form.html', vehicle=vehicle, record=None)

@maintenance_bp.route('/maintenance/<int:m_id>/edit', methods=['GET', 'POST'])
def edit(m_id):
    record = MaintenanceRecord.get_by_id(m_id)
    if not record:
        flash('找不到該紀錄', 'danger')
        return redirect(url_for('garage.index'))
        
    v_id = record['vehicle_id']
    vehicle = Vehicle.get_by_id(v_id)
        
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        mileage_at_service = request.form.get('mileage_at_service', type=int)
        interval_mileage = request.form.get('interval_mileage', type=int)
        cost = request.form.get('cost', type=int, default=0)
        service_date = request.form.get('service_date')
        notes = request.form.get('notes', '')
        
        if not item_name or mileage_at_service is None or not service_date:
            flash('請填寫必填欄位（項目、里程、日期）', 'danger')
            return render_template('maintenance/form.html', vehicle=vehicle, record=record)
            
        MaintenanceRecord.update(m_id, item_name, mileage_at_service, interval_mileage, cost, service_date, notes)
        flash('保養紀錄已更新', 'success')
        return redirect(url_for('maintenance.index', v_id=v_id))
        
    return render_template('maintenance/form.html', vehicle=vehicle, record=record)

@maintenance_bp.route('/maintenance/<int:m_id>/delete', methods=['POST'])
def delete(m_id):
    record = MaintenanceRecord.get_by_id(m_id)
    if record:
        v_id = record['vehicle_id']
        MaintenanceRecord.delete(m_id)
        flash('保養紀錄已刪除', 'success')
        return redirect(url_for('maintenance.index', v_id=v_id))
    return redirect(url_for('garage.index'))
