from flask import Blueprint, render_template, redirect, url_for, session, request
from app.db import get_db_connetction

payment_bp = Blueprint('payment', __name__)

@payment_bp.route("/payment_page/<booking_id>")
def confirme_payment(booking_id):
    if "user_id" not in session:
        return redirect(url_for('auth.login', next=request.url))
    return render_template('payment.html', booking_id=booking_id)
    
    