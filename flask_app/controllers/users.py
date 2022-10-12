from flask import redirect, request, render_template, session, url_for
from flask_app import app
from flask_app.models.user import User

@app.route('/')
def create():
    return render_template('create.html', info=session)

@app.route('/users/')
def users():
    return render_template('read_all.html', users=User.get_all())

@app.route('/user/create/', methods=['POST'])
def create_user():
    users = User.get_all()
    print(users)
    if not User.validate_user(request.form,users):
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        return redirect('/')
    user_id = User.save(request.form)
    session.clear()
    return redirect(url_for('show_user', id=user_id))

@app.route('/user/show/<int:id>')
def show_user(id):
    data = {
        "id" : id
    }
    return render_template('read_one.html', user=User.get_one(data))

# @app.route('/user/show/')
# def show_user_wo_id():
#     data = {
#         "email" : session['email']
#     }
#     return render_template('read_one.html', user=User.get_one_by_email(data))

@app.route('/user/edit/<int:id>')
def edit(id):
    data = {
        'id' : id
    }
    return render_template('edit.html', user = User.get_one(data))

@app.route('/user/update/<int:id>', methods=['POST'])
def update(id):
    User.update(request.form)
    return redirect(url_for('show_user', user_id=id))

@app.route('/user/destroy/<id>')
def delete_user(id):
    data = {
        "id" : id
    }
    User.delete(data)
    return redirect('/users/')





