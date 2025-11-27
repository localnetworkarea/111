from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
from datetime import datetime
from functools import wraps
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'homework'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'materials'), exist_ok=True)

# Database initialization
def init_db():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Classes table
    c.execute('''CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        teacher_id INTEGER,
        class_date TIMESTAMP,
        meeting_link TEXT,
        status TEXT DEFAULT 'scheduled',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (teacher_id) REFERENCES users(id)
    )''')
    
    # Homework table
    c.execute('''CREATE TABLE IF NOT EXISTS homework (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER,
        student_id INTEGER,
        teacher_id INTEGER,
        title TEXT NOT NULL,
        description TEXT,
        file_path TEXT,
        submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'pending',
        grade TEXT,
        feedback TEXT,
        FOREIGN KEY (class_id) REFERENCES classes(id),
        FOREIGN KEY (student_id) REFERENCES users(id),
        FOREIGN KEY (teacher_id) REFERENCES users(id)
    )''')
    
    # Enrollments table
    c.execute('''CREATE TABLE IF NOT EXISTS enrollments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        class_id INTEGER,
        enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES users(id),
        FOREIGN KEY (class_id) REFERENCES classes(id)
    )''')
    
    # Class materials table
    c.execute('''CREATE TABLE IF NOT EXISTS class_materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER,
        title TEXT NOT NULL,
        file_path TEXT,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (class_id) REFERENCES classes(id)
    )''')

    # Attendance table
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER,
        student_id INTEGER,
        date DATE,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (class_id) REFERENCES classes(id),
        FOREIGN KEY (student_id) REFERENCES users(id)
    )''')
    
    # Create default admin if not exists
    c.execute("SELECT * FROM users WHERE username = ?", ('admin',))
    if not c.fetchone():
        admin_password = generate_password_hash('admin123')
        c.execute("INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
                  ('admin', admin_password, 'مدیر سیستم', 'admin'))
    
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect('school.db')
    conn.row_factory = sqlite3.Row
    return conn

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Role required decorator
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] not in roles:
                flash('دسترسی غیرمجاز', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def index():
    if 'user_id' in session:
        role = session.get('role')
        if role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif role == 'teacher':
            return redirect(url_for('teacher_dashboard'))
        elif role == 'student':
            return redirect(url_for('student_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            session['role'] = user['role']
            flash('ورود موفقیت‌آمیز بود', 'success')
            return redirect(url_for('index'))
        else:
            flash('نام کاربری یا رمز عبور اشتباه است', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('خروج موفقیت‌آمیز بود', 'success')
    return redirect(url_for('login'))

# Admin routes
@app.route('/admin')
@login_required
@role_required('admin')
def admin_dashboard():
    conn = get_db()
    students = conn.execute('SELECT * FROM users WHERE role = "student"').fetchall()
    teachers = conn.execute('SELECT * FROM users WHERE role = "teacher"').fetchall()
    classes = conn.execute('''
        SELECT c.*, u.full_name as teacher_name 
        FROM classes c 
        LEFT JOIN users u ON c.teacher_id = u.id
    ''').fetchall()
    conn.close()
    
    return render_template('admin_dashboard.html', 
                         students=students, 
                         teachers=teachers, 
                         classes=classes)

@app.route('/admin/add_user', methods=['POST'])
@login_required
@role_required('admin')
def add_user():
    username = request.form['username']
    password = generate_password_hash(request.form['password'])
    full_name = request.form['full_name']
    role = request.form['role']
    
    conn = get_db()
    try:
        conn.execute('INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)',
                    (username, password, full_name, role))
        conn.commit()
        flash('کاربر با موفقیت اضافه شد', 'success')
    except sqlite3.IntegrityError:
        flash('نام کاربری تکراری است', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_user/<int:user_id>')
@login_required
@role_required('admin')
def delete_user(user_id):
    conn = get_db()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    flash('کاربر با موفقیت حذف شد', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit_user/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def edit_user(user_id):
    full_name = request.form['full_name']
    username = request.form['username']
    
    conn = get_db()
    conn.execute('UPDATE users SET full_name = ?, username = ? WHERE id = ?',
                (full_name, username, user_id))
    
    if request.form.get('new_password'):
        password = generate_password_hash(request.form['new_password'])
        conn.execute('UPDATE users SET password = ? WHERE id = ?', (password, user_id))
    
    conn.commit()
    conn.close()
    flash('اطلاعات کاربر به‌روزرسانی شد', 'success')
    return redirect(url_for('admin_dashboard'))

# Teacher routes
@app.route('/teacher')
@login_required
@role_required('teacher')
def teacher_dashboard():
    conn = get_db()
    classes = conn.execute('SELECT * FROM classes WHERE teacher_id = ?', 
                          (session['user_id'],)).fetchall()
    
    homework_list = conn.execute('''
        SELECT h.*, u.full_name as student_name, c.title as class_title
        FROM homework h
        JOIN users u ON h.student_id = u.id
        JOIN classes c ON h.class_id = c.id
        WHERE h.teacher_id = ?
        ORDER BY h.submission_date DESC
    ''', (session['user_id'],)).fetchall()
    
    conn.close()
    return render_template('teacher_dashboard.html', 
                         classes=classes, 
                         homework_list=homework_list)

@app.route('/teacher/create_class', methods=['POST'])
@login_required
@role_required('teacher')
def create_class():
    title = request.form['title']
    description = request.form['description']
    class_date = request.form['class_date']
    meeting_link = request.form.get('meeting_link', '')
    
    conn = get_db()
    conn.execute('''INSERT INTO classes (title, description, teacher_id, class_date, meeting_link)
                    VALUES (?, ?, ?, ?, ?)''',
                (title, description, session['user_id'], class_date, meeting_link))
    conn.commit()
    conn.close()
    
    flash('کلاس با موفقیت ایجاد شد', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/class/<int:class_id>')
@login_required
@role_required('teacher')
def teacher_class_view(class_id):
    conn = get_db()
    class_info = conn.execute('SELECT * FROM classes WHERE id = ? AND teacher_id = ?',
                             (class_id, session['user_id'])).fetchone()
    
    if not class_info:
        flash('کلاس یافت نشد', 'error')
        conn.close()
        return redirect(url_for('teacher_dashboard'))
    
    students = conn.execute('''
        SELECT u.* FROM users u
        JOIN enrollments e ON u.id = e.student_id
        WHERE e.class_id = ?
    ''', (class_id,)).fetchall()
    
    materials = conn.execute('SELECT * FROM class_materials WHERE class_id = ?',
                            (class_id,)).fetchall()
    
    conn.close()
    return render_template('teacher_class.html', 
                         class_info=class_info, 
                         students=students,
                         materials=materials)

@app.route('/teacher/verify_homework/<int:homework_id>', methods=['POST'])
@login_required
@role_required('teacher')
def verify_homework(homework_id):
    status = request.form['status']
    grade = request.form.get('grade', '')
    feedback = request.form.get('feedback', '')
    
    conn = get_db()
    conn.execute('''UPDATE homework SET status = ?, grade = ?, feedback = ?
                    WHERE id = ? AND teacher_id = ?''',
                (status, grade, feedback, homework_id, session['user_id']))
    conn.commit()
    conn.close()
    
    flash('تکلیف با موفقیت بررسی شد', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/upload_material/<int:class_id>', methods=['POST'])
@login_required
@role_required('teacher')
def upload_material(class_id):
    if 'file' not in request.files:
        flash('فایلی انتخاب نشده است', 'error')
        return redirect(url_for('teacher_class_view', class_id=class_id))
    
    file = request.files['file']
    if file.filename == '':
        flash('فایلی انتخاب نشده است', 'error')
        return redirect(url_for('teacher_class_view', class_id=class_id))
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'materials', filename)
        file.save(filepath)
        
        title = request.form.get('title', filename)
        
        conn = get_db()
        conn.execute('INSERT INTO class_materials (class_id, title, file_path) VALUES (?, ?, ?)',
                    (class_id, title, filepath))
        conn.commit()
        conn.close()
        
        flash('فایل با موفقیت آپلود شد', 'success')
    
    return redirect(url_for('teacher_class_view', class_id=class_id))

@app.route('/teacher/class/<int:class_id>/attendance', methods=['GET', 'POST'])
@login_required
@role_required('teacher')
def teacher_attendance(class_id):
    conn = get_db()
    
    # Verify teacher owns the class
    class_info = conn.execute('SELECT * FROM classes WHERE id = ? AND teacher_id = ?',
                             (class_id, session['user_id'])).fetchone()
    if not class_info:
        conn.close()
        flash('کلاس یافت نشد', 'error')
        return redirect(url_for('teacher_dashboard'))

    if request.method == 'POST':
        date = request.form['date']
        
        # Delete existing attendance for this date to allow updates
        conn.execute('DELETE FROM attendance WHERE class_id = ? AND date = ?',
                    (class_id, date))
        
        # Save new attendance
        for key, value in request.form.items():
            if key.startswith('status_'):
                student_id = key.split('_')[1]
                conn.execute('''INSERT INTO attendance (class_id, student_id, date, status)
                              VALUES (?, ?, ?, ?)''',
                           (class_id, student_id, date, value))
        
        conn.commit()
        flash('حضور و غیاب با موفقیت ثبت شد', 'success')
        conn.close()
        return redirect(url_for('teacher_attendance', class_id=class_id))
    
    # GET request
    students = conn.execute('''
        SELECT u.*, a.status as today_status
        FROM users u
        JOIN enrollments e ON u.id = e.student_id
        LEFT JOIN attendance a ON u.id = a.student_id AND a.class_id = ? AND a.date = ?
        WHERE e.class_id = ?
    ''', (class_id, datetime.now().strftime('%Y-%m-%d'), class_id)).fetchall()
    
    conn.close()
    return render_template('teacher_attendance.html', 
                         class_info=class_info, 
                         students=students,
                         today=datetime.now().strftime('%Y-%m-%d'))

# Student routes
@app.route('/student')
@login_required
@role_required('student')
def student_dashboard():
    conn = get_db()
    
    # Get enrolled classes
    classes = conn.execute('''
        SELECT c.*, u.full_name as teacher_name
        FROM classes c
        JOIN enrollments e ON c.id = e.class_id
        JOIN users u ON c.teacher_id = u.id
        WHERE e.student_id = ?
    ''', (session['user_id'],)).fetchall()
    
    # Get homework submissions
    homework_list = conn.execute('''
        SELECT h.*, c.title as class_title
        FROM homework h
        JOIN classes c ON h.class_id = c.id
        WHERE h.student_id = ?
        ORDER BY h.submission_date DESC
    ''', (session['user_id'],)).fetchall()
    
    # Get available classes to enroll
    available_classes = conn.execute('''
        SELECT c.*, u.full_name as teacher_name
        FROM classes c
        JOIN users u ON c.teacher_id = u.id
        WHERE c.id NOT IN (
            SELECT class_id FROM enrollments WHERE student_id = ?
        )
    ''', (session['user_id'],)).fetchall()
    
    conn.close()
    return render_template('student_dashboard.html', 
                         classes=classes, 
                         homework_list=homework_list,
                         available_classes=available_classes)

@app.route('/student/enroll/<int:class_id>')
@login_required
@role_required('student')
def enroll_class(class_id):
    conn = get_db()
    try:
        conn.execute('INSERT INTO enrollments (student_id, class_id) VALUES (?, ?)',
                    (session['user_id'], class_id))
        conn.commit()
        flash('با موفقیت در کلاس ثبت‌نام شدید', 'success')
    except sqlite3.IntegrityError:
        flash('شما قبلاً در این کلاس ثبت‌نام کرده‌اید', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('student_dashboard'))

@app.route('/student/class/<int:class_id>')
@login_required
@role_required('student')
def student_class_view(class_id):
    conn = get_db()
    
    # Check enrollment
    enrollment = conn.execute('''
        SELECT * FROM enrollments 
        WHERE student_id = ? AND class_id = ?
    ''', (session['user_id'], class_id)).fetchone()
    
    if not enrollment:
        flash('شما در این کلاس ثبت‌نام نکرده‌اید', 'error')
        conn.close()
        return redirect(url_for('student_dashboard'))
    
    class_info = conn.execute('''
        SELECT c.*, u.full_name as teacher_name
        FROM classes c
        JOIN users u ON c.teacher_id = u.id
        WHERE c.id = ?
    ''', (class_id,)).fetchone()
    
    materials = conn.execute('SELECT * FROM class_materials WHERE class_id = ?',
                            (class_id,)).fetchall()
    
    homework_list = conn.execute('''
        SELECT * FROM homework 
        WHERE class_id = ? AND student_id = ?
    ''', (class_id, session['user_id'])).fetchall()
    
    conn.close()
    return render_template('student_class.html', 
                         class_info=class_info,
                         materials=materials,
                         homework_list=homework_list)

@app.route('/student/submit_homework/<int:class_id>', methods=['POST'])
@login_required
@role_required('student')
def submit_homework(class_id):
    title = request.form['title']
    description = request.form.get('description', '')
    
    conn = get_db()
    teacher_id = conn.execute('SELECT teacher_id FROM classes WHERE id = ?', 
                             (class_id,)).fetchone()['teacher_id']
    
    file_path = None
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'homework', 
                                    f"{session['user_id']}_{datetime.now().timestamp()}_{filename}")
            file.save(file_path)
    
    conn.execute('''INSERT INTO homework (class_id, student_id, teacher_id, title, description, file_path)
                    VALUES (?, ?, ?, ?, ?, ?)''',
                (class_id, session['user_id'], teacher_id, title, description, file_path))
    conn.commit()
    conn.close()
    
    flash('تکلیف با موفقیت ارسال شد', 'success')
    return redirect(url_for('student_class_view', class_id=class_id))

@app.route('/student/attendance')
@login_required
@role_required('student')
def student_attendance():
    conn = get_db()
    
    attendance_records = conn.execute('''
        SELECT a.*, c.title as class_title, u.full_name as teacher_name
        FROM attendance a
        JOIN classes c ON a.class_id = c.id
        JOIN users u ON c.teacher_id = u.id
        WHERE a.student_id = ?
        ORDER BY a.date DESC
    ''', (session['user_id'],)).fetchall()
    
    conn.close()
    return render_template('student_attendance.html', 
                         attendance_records=attendance_records)

@app.route('/download/<path:filename>')
@login_required
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
