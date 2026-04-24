from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.vehicle import Vehicle
from app.models.wishlist import WishlistItem

wishlist_bp = Blueprint('wishlist', __name__, url_prefix='/wishlist')

@wishlist_bp.route('/')
def index():
    vehicles = Vehicle.get_all()
    # 建立以車輛 ID 區分的願望清單
    wishlists_by_vehicle = {}
    total_budget = 0
    total_spent = 0
    
    for v in vehicles:
        items = WishlistItem.get_by_vehicle(v['id'])
        if items:
            wishlists_by_vehicle[v] = items
            for item in items:
                if item['is_installed'] == 1:
                    total_spent += item['estimated_cost']
                else:
                    total_budget += item['estimated_cost']
                    
    return render_template('wishlist/index.html', 
                          wishlists_by_vehicle=wishlists_by_vehicle,
                          total_budget=total_budget,
                          total_spent=total_spent)

@wishlist_bp.route('/add', methods=['GET', 'POST'])
def add():
    vehicles = Vehicle.get_all()
    if not vehicles:
        flash('請先至車庫新增至少一台車輛！', 'warning')
        return redirect(url_for('garage.index'))
        
    if request.method == 'POST':
        vehicle_id = request.form.get('vehicle_id', type=int)
        item_name = request.form.get('item_name')
        estimated_cost = request.form.get('estimated_cost', type=int, default=0)
        
        if not vehicle_id or not item_name:
            flash('請填寫必填欄位', 'danger')
            return render_template('wishlist/form.html', vehicles=vehicles, item=None)
            
        WishlistItem.create(vehicle_id, item_name, estimated_cost)
        flash('已加入願望清單', 'success')
        return redirect(url_for('wishlist.index'))
        
    return render_template('wishlist/form.html', vehicles=vehicles, item=None)

@wishlist_bp.route('/<int:w_id>/edit', methods=['GET', 'POST'])
def edit(w_id):
    item = WishlistItem.get_by_id(w_id)
    if not item:
        return redirect(url_for('wishlist.index'))
        
    vehicles = Vehicle.get_all()
    
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        estimated_cost = request.form.get('estimated_cost', type=int, default=0)
        is_installed = 1 if request.form.get('is_installed') == 'on' else 0
        
        if not item_name:
            flash('請填寫必填欄位', 'danger')
            return render_template('wishlist/form.html', vehicles=vehicles, item=item)
            
        WishlistItem.update(w_id, item_name, estimated_cost, is_installed)
        flash('願望項目已更新', 'success')
        return redirect(url_for('wishlist.index'))
        
    return render_template('wishlist/form.html', vehicles=vehicles, item=item)

@wishlist_bp.route('/<int:w_id>/toggle', methods=['POST'])
def toggle(w_id):
    item = WishlistItem.get_by_id(w_id)
    if item:
        new_status = 0 if item['is_installed'] == 1 else 1
        WishlistItem.toggle_status(w_id, new_status)
    return redirect(url_for('wishlist.index'))

@wishlist_bp.route('/<int:w_id>/delete', methods=['POST'])
def delete(w_id):
    WishlistItem.delete(w_id)
    flash('項目已刪除', 'success')
    return redirect(url_for('wishlist.index'))
