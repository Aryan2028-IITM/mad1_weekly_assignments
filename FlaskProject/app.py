import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


current_dir=os.path.dirname(__file__)
app =    Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(current_dir,'database.sqlite3')
db=SQLAlchemy()
db.init_app(app)
app.app_context().push()


class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number= db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String , nullable=False)
    last_name = db.Column(db.String)

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String, nullable=False, unique=True)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)

class Enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estudent_id= db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    ecourse_id=db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)

for i in Student.query.all():
    @app.route('/student/'+str(i.student_id), methods=['GET'])
    def student():

        return render_template('student.html',i=i)

    @app.route('/student/'+str(i.student_id)+'/delete', methods=['GET'])
    def delete():

        sid = i.student_id
        stdent = Student.query.filter_by(student_id=sid).first()
        db.session.delete(stdent)
        db.session.commit()
        return 'Student Deleted'
    @app.route('/student/'+str(i.student_id)+'/update', methods=['GET'])
    def update(student_id):
        if request.method == 'GET':
            return render_template('update.html')
        elif request.method == 'POST':
            sid = student_id
            roll_number = request.form['roll']
            first_name = request.form['f_name']
            last_name = request.form['l_name']
            stdent = Student.query.filter_by(student_id=sid).first()
            stdent.roll_number = roll_number
            stdent.first_name = first_name
            stdent.last_name = last_name
            db.session.commit()
            return 'Student Updated'

@app.route('/', methods=['POST','GET'])
def index():

    if request.method=='GET':
        if Student.query.all():
            stu=Student.query.all()
            return render_template('home.html',Student=stu)
        return render_template('index.html')
    
@app.route('/student/create', methods=['POST','GET'])
def create():
    if request.method=='GET':
        return render_template('create.html')
    elif request.method=='POST':
        roll_number=request.form['roll']
        first_name=request.form['f_name']
        last_name=request.form['l_name']
        c=request.form.getlist('courses')
        stdent=Student(roll_number=roll_number,first_name=first_name,last_name=last_name)
        for v in c:
            enroll=Enrollments(estudent_id=stdent.student_id,ecourse_id=v[-1])
            if Student.query.filter_by(roll_number=roll_number).first():
                return render_template('exists.html')
            else:
                db.session.add(stdent,enroll)


                db.session.commit()

if __name__ == '__main__':
    app.run()
