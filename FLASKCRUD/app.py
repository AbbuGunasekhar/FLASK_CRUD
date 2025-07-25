from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/FLASK/guna.db' # relative path



db=SQLAlchemy(app)


class ToDo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    completed=db.Column(db.Integer,default=0)
    def __repr__(self):
        return '<Task %r>' % self.id 

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        task_content=request.form['content']
        new_task=ToDo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()

            return redirect('/')
        except:
            return 'There was an error'
    else:
        tasks =ToDo.query.order_by(ToDo.date_created).all()
        return render_template('index.html',tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem in delete"
    
@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    task=ToDo.query.get_or_404(id)
    if request.method=='POST':
        task_content=request.form['content']
        try:
            task.content = task_content
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue in upating the task"
    else:
        return render_template('update.html',task=task)
if(__name__=="__main__"):
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)