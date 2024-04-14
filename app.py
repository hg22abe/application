from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from sqlite3 import Error
import os
import cv2




def create_app(test_config=None):
    



     



    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/cam')
    def camera():
        while True:
            cv2.VideoCapture(0)

        return "done"

            
    
    @app.route('/appointments')
    def appointments():
        return render_template("index.html", 'index')
    
    @app.route('/', methods=("GET",))
    def inp():
        return render_template("in.html")

    @app.route('/addpatient', methods=("POST",))
    def add_new_patient():

        conn = None
        try:
           conn = sqlite3.connect("patient.db")
        except Error as e:
            return "Error connecting to the database"
    
        try:
            current = conn.cursor()
            query = "INSERT INTO patient (name, password) VALUES (?, ?)"
            values = request.form['username'], request.form['password']
            current.execute(query, values)
            conn.commit
            current.close()
        except Error as e:
            return "Error making the query" + str(e)
        finally:
            conn.close

        return render_template("opt.html")
    
    
    
    @app.route('/addpatient/time', methods=("POST",))
    def patient():
        selected_day = request.form['selected_day']
        selected_time = request.form['selected_time']
        return render_template("res.html", day=selected_day, time=selected_time)



    

        
    
    


    return app

    




app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
