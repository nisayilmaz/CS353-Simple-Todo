
import re
import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime, timedelta


app = Flask(__name__)

app.secret_key = 'abcdefgh'

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'cs353hw4db'

mysql = MySQL(app)


@app.route('/', methods=['GET'])
def mainpage():
    return render_template('mainpage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and not session.get('loggedin'):
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM User WHERE username = % s AND password = % s', (username, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            message = 'Logged in successfully!'
            return redirect(url_for('tasks'))
        else:
            message = 'Please enter correct email / password !'
    if not session.get('loggedin'):
        return render_template('login.html', message=message)
    else:
        return redirect(url_for('tasks'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if  session.get('loggedin'):
        return redirect(url_for('tasks'))
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            message = 'Choose a different username!'

        elif not username or not password or not email:
            message = 'Please fill out the form!'

        else:
            cursor.execute(
                'INSERT INTO User (id, username, email, password) VALUES (NULL, % s, % s, % s)', (username, email, password,))
            mysql.connection.commit()
            message = 'User successfully created!'

    elif request.method == 'POST':

        message = 'Please fill all the fields!'
    return render_template('register.html', message=message)


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if not session.get('loggedin'):
        return redirect(url_for('login'))
    message = ''
    if 'message' in session.keys():
        message = session.get('message')
        session.pop('message')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select * from TaskType')
    types = cursor.fetchall()
    cursor.execute('SELECT id FROM User WHERE username = % s',
                   (session['username'], ))
    id = cursor.fetchone()
    current_time = datetime.now() + timedelta(hours=3)
    cursor.execute(
        'select * from Task where user_id = %s order by abs(timediff(%s , deadline)) asc, creation_time asc', (id.get('id'), current_time))
    all_tasks = cursor.fetchall()

    cursor.execute(
        'select * from Task where user_id = %s and status = %s order by abs(timediff(%s , deadline)) asc, creation_time asc', (id.get('id'), "Todo", current_time))
    unfinished_tasks = cursor.fetchall()

    cursor.execute(
        'select * from Task where user_id = %s and status = %s order by done_time desc, creation_time asc', (id.get('id'), "Done"))
    finished_tasks = cursor.fetchall()

    if request.method == 'POST':
        cursor.execute('SELECT id FROM User WHERE username = % s',
                       (session['username'], ))
        id = cursor.fetchone()

        if 'title' in request.form and 'description' in request.form and 'deadline' in request.form and 'type' in request.form:
            title = request.form['title']
            description = request.form['description']
            deadline = request.form['deadline']
            type = request.form['type']
            if datetime.strptime(deadline, '%Y-%m-%dT%H:%M') > datetime.now() + timedelta(hours=3):
                cursor.execute('insert into Task (title, description, status, deadline, creation_time, done_time, user_id, task_type) values (%s, %s, "Todo", %s, %s, NULL, %s, %s)', (
                    title, description, deadline, datetime.now() + timedelta(hours=3), id['id'], type))
                mysql.connection.commit()
                return redirect(url_for('tasks'))

            else:
                message = 'Enter a valid deadline!'
        else:
            message = 'Fill all the required fields'
    return render_template('tasks.html', types=types, all_tasks=all_tasks, unfinished=unfinished_tasks, finished=finished_tasks, message=message)


@app.route('/complete/<id>', methods=['GET', 'POST'])
def complete(id):
    if not session.get('loggedin'):
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    now = datetime.now() + timedelta(hours=3)
    cursor.execute('update Task set status = "Done", done_time = %s where id= %s',
                   (now.strftime('%Y-%m-%d %H:%M:%S'), id))
    mysql.connection.commit()
    return redirect(url_for('tasks'))


@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if not session.get('loggedin'):
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id FROM User WHERE username = % s',
                   (session['username'], ))
    id = cursor.fetchone()
    cursor.execute("""select title, concat(
   floor(hour(timediff(done_time, deadline)) / 24), ' days, ',
   mod(hour(timediff(done_time, deadline)), 24), ' hours, ',
   minute(timediff(done_time, deadline)), ' minutes, ',
   second(timediff(done_time, deadline)), ' seconds') as difference from Task where user_id = %s and done_time > deadline and status = %s order by deadline asc""", (id.get('id'), "Done"))
    late_tasks = cursor.fetchall()

    cursor.execute("""select concat(
   floor(hour(avg_time) / 24), ' days, ',
   mod(hour(avg_time), 24), ' hours, ',
   minute(avg_time), ' minutes, ',
   second(avg_time), ' seconds') as avg_time from (select avg(timediff(done_time, creation_time)) as avg_time from Task where user_id = %s and status = %s) as T""", (id.get('id'), "Done"))
    avg_time = cursor.fetchone()

    cursor.execute("""select task_type, count(*) as cnt from Task where user_id = %s and status = %s group by task_type order by cnt desc""", (id.get('id'), "Done"))
    type_count = cursor.fetchall()

    cursor.execute("""select title, deadline from Task where user_id = %s and status = %s order by deadline asc""", (id.get('id'), "Todo"))
    deadline = cursor.fetchall()

    cursor.execute("""select title, concat(
   floor(hour(timediff(done_time, creation_time)) / 24), ' days, ',
   mod(hour(timediff(done_time, creation_time)), 24), ' hours, ',
   minute(timediff(done_time, creation_time)), ' minutes, ',
   second(timediff(done_time, creation_time)), ' seconds') as duration from Task where user_id = %s and status = %s order by duration desc limit 2""", (id.get('id'), "Done"))
    longest = cursor.fetchall()


    return render_template('analysis.html', late_tasks=late_tasks, time=avg_time, type_count=type_count, deadline=deadline, longest=longest)


@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    if not session.get('loggedin'):
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('delete from Task where id = %s', (id,))
    mysql.connection.commit()
    return redirect(url_for('tasks'))


@app.route('/edit/<id>', methods=['POST'])
def edit(id):
    if not session.get('loggedin'):
        return redirect(url_for('login'))
    vars = {}
    sql = ''
    vars['title'] = request.form['title']
    vars['description'] = request.form['description']
    vars['deadline'] = request.form['deadline']
    vars['task_type'] = request.form['task_type']
    for key, value in vars.items():
        if value != '':
            sql += key + '="' + value + '" ,'
    if vars['deadline'] and datetime.strptime(vars['deadline'], '%Y-%m-%dT%H:%M') < datetime.now() + timedelta(hours=3):
        session['message'] = 'Enter valid deadline!'
        return redirect(url_for('tasks'))
    sql = sql[0:len(sql) - 1]
    if sql != '':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = 'update Task set ' + sql + ' where id = ' + id
        cursor.execute(sql)
        mysql.connection.commit()
    return redirect(url_for('tasks'))


@app.route('/logout', methods=['POST'])
def logout():
    if not session.get('loggedin'):
        return redirect(url_for('login'))
    if session.get('loggedin'):
        session.pop('loggedin')
        session.pop('userid')
        session.pop('username')
        session.pop('email')
        return redirect(url_for('mainpage'))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
