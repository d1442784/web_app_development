from flask import Blueprint, render_template, request, redirect, url_for

wishlist_bp = Blueprint('wishlist', __name__, url_prefix='/wishlist')

@wishlist_bp.route('/')
def index():
    """
    GET /wishlist/
    願望清單列表
    - 取得所有願望清單 (WishlistItem.get_by_vehicle 或全域取得，視實作細節而定)
    - 計算預估總花費
    - 渲染 wishlist/index.html
    """
    pass

@wishlist_bp.route('/add', methods=['GET', 'POST'])
def add():
    """
    GET/POST /wishlist/add
    新增願望清單項目
    - GET: 渲染 wishlist/form.html
    - POST: 接收表單，呼叫 WishlistItem.create()，重導向至 /wishlist/
    """
    pass

@wishlist_bp.route('/<int:w_id>/edit', methods=['GET', 'POST'])
def edit(w_id):
    """
    GET/POST /wishlist/<w_id>/edit
    編輯願望清單項目
    - GET: 取得該項目 (WishlistItem.get_by_id)，渲染 wishlist/form.html
    - POST: 接收表單，呼叫 WishlistItem.update()，重導向至 /wishlist/
    """
    pass

@wishlist_bp.route('/<int:w_id>/toggle', methods=['POST'])
def toggle(w_id):
    """
    POST /wishlist/<w_id>/toggle
    切換願望清單的安裝狀態
    - 取得該項目，反轉 is_installed 狀態
    - 呼叫 WishlistItem.toggle_status()
    - 重導向至 /wishlist/
    """
    pass

@wishlist_bp.route('/<int:w_id>/delete', methods=['POST'])
def delete(w_id):
    """
    POST /wishlist/<w_id>/delete
    刪除願望清單項目
    - 呼叫 WishlistItem.delete()
    - 重導向至 /wishlist/
    """
    pass
