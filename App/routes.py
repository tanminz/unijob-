
import uuid
import os
import json
from flask import Blueprint, render_template, request, redirect, url_for, session
from App.utils.json_connector import load_json, save_json
from werkzeug.utils import secure_filename
from flask import current_app


main = Blueprint('main', __name__)

# -------------------- JSON Utilities --------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')

def load_json(filename):
    filepath = os.path.join(DATA_PATH, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filename, data):
    filepath = os.path.join(DATA_PATH, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# -------------------- ROUTES --------------------

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['login_user']
        password = request.form['login_pass']
        role = request.form['role']

        users = load_json('users.json')
        user = next((u for u in users if u['email'] == email and u['password'] == password and u['role'] == role), None)

        if not user:
            error = "Sai thông tin đăng nhập. Vui lòng kiểm tra lại."
            return render_template('login.html', error=error)

        if user['role'] == 'employer' and user['status'] != 'approved':
            error = "Tài khoản của bạn đang chờ phê duyệt bởi CTSV."
            return render_template('login.html', error=error)

        session['user'] = user
        return redirect(url_for('main.index'))

    return render_template('login.html', error=None)




from werkzeug.utils import secure_filename
from flask import current_app
import os

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        admin_code = request.form.get('admin_code', '')  # lấy mã admin nếu có

        # ✅ Nếu chọn vai trò là admin thì bắt buộc phải nhập đúng mã
        if role == 'admin':
            if admin_code != current_app.config['ADMIN_VERIFICATION_CODE']:
                error = "Mã xác thực admin không đúng."
                return render_template('register.html', error=error)
        # Thông tin bổ sung
        company_name = request.form.get('company_name', '')
        license_file = request.files.get('license')

        # Mặc định trạng thái = approved nếu không phải employer
        status = 'pending' if role == 'employer' else 'approved'

        # Lưu giấy phép
        license_filename = ''
        if role == 'employer' and license_file:
            filename = secure_filename(email + '_' + license_file.filename)
            license_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

            # ✅ Tạo thư mục nếu chưa có
            os.makedirs(os.path.dirname(license_path), exist_ok=True)

            # ✅ Lưu file vào thư mục
            license_file.save(license_path)
            license_filename = filename

        # Tạo user mới
        new_user = {
            "id": email,
            "fullname": fullname,
            "email": email,
            "password": password,
            "role": role,
            "status": status,
            "company_name": company_name,
            "license": license_filename
        }

        users = load_json('users.json')
        users.append(new_user)
        save_json('users.json', users)

        return redirect(url_for('main.login'))

    return render_template('register.html')


@main.route('/admin/employers')
def admin_employers():
    # Kiểm tra đăng nhập và vai trò
    if 'user' not in session or session['user']['role'] != 'admin':
        return redirect(url_for('main.login'))

    users = load_json('users.json')
    employers = [u for u in users if u['role'] == 'employer' and u['status'] == 'pending']
    return render_template('admin_employers.html', employers=employers)

@main.route('/admin/approve', methods=['POST'])
def approve_employer():
    email = request.form['email']
    users = load_json('users.json')
    for u in users:
        if u['email'] == email and u['role'] == 'employer':
            u['status'] = 'approved'
            break
    save_json('users.json', users)
    return redirect(url_for('main.admin_employers'))


# -------------------- Static Pages --------------------
@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/faq')
def faq():
    return render_template('faq.html')

@main.route('/gallery')
def gallery():
    return render_template('gallery.html')

@main.route('/job-listings')
def job_listings():
    return render_template('job-listings.html')

@main.route('/job-single')
def job_single():
    return render_template('job-single.html')

@main.route('/post-job')
def post_job():
    return render_template('post-job.html')

@main.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@main.route('/portfolio-single')
def portfolio_single():
    return render_template('portfolio-single.html')

@main.route('/services')
def services():
    return render_template('services.html')

@main.route('/service-single')
def service_single():
    return render_template('service-single.html')

@main.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@main.route('/blog')
def blog():
    return render_template('blog.html')

@main.route('/blog-single')
def blog_single():
    return render_template('blog-single.html')

@main.route('/main')
def main_page():
    return render_template('main.html')
