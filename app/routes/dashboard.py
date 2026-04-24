from flask import Blueprint, render_template
from app.models.vehicle import Vehicle
from app.models.maintenance import MaintenanceRecord

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    vehicles = Vehicle.get_all()
    due_items = []
    
    for v in vehicles:
        items = MaintenanceRecord.get_due_maintenance(v['id'], v['current_mileage'])
        for item in items:
            item['vehicle_name'] = f"{v['brand']} {v['model_name']}"
            due_items.append(item)
            
    return render_template('dashboard/index.html', due_items=due_items, vehicles=vehicles)
