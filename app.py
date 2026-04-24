from flask import Flask
from app.routes.dashboard import dashboard_bp
from app.routes.garage import garage_bp
from app.routes.maintenance import maintenance_bp
from app.routes.wishlist import wishlist_bp

app = Flask(__name__)
# 實務上應使用環境變數，此處為了方便展示直接設定
app.secret_key = 'super_secret_moto_key'

# 註冊 Blueprints
app.register_blueprint(dashboard_bp)
app.register_blueprint(garage_bp)
app.register_blueprint(maintenance_bp)
app.register_blueprint(wishlist_bp)

if __name__ == '__main__':
    app.run(debug=True)
