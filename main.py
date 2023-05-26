from flask import Flask, render_template, request, session, url_for, redirect, flash
import mysql.connector

app = Flask('app')
app.secret_key = "mysecretkey"

# Establish MySQL connection
mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
)


@app.route('/reset', methods=['GET', 'POST'])
def reset():
  
        cursor = mydb.cursor(dictionary=True)

        with open('store_schema.sql', 'r') as f:
            script = f.read()

        # Split the script by semicolon to separate individual SQL statements
        statements = script.split(';')

        # Execute each SQL statement separately
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)

        mydb.commit()

        return redirect(url_for('index'))


#Login and Register and Homepage--------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    mydb = mysql.connector.connect(
        host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
        user="admin",
        password="tommyzackmaya",
        database="university"
    )

    if request.method == 'POST':
        cursor =  mydb.cursor(dictionary=True)
        username = request.form["username"]
        password = request.form["password"]
        view = request.form.get("view")

        cursor.execute("SELECT uid FROM user WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
   
        if user != None:
            session['role'] = view
            session['user_id'] = user['uid']
            session['logged in'] = True
            session['uName'] = username
            session['uPass'] = password

            if(session['role'] ==  'student'):
                cursor.execute("SELECT studentid, program FROM student WHERE studentid = %s ", (session['user_id'],))
                uid = cursor.fetchone()
                if uid == None:
                   return render_template('login.html', error="You selected the wrong login view")
                session['semester'] = "Spring"
                session['year'] = "2023"
                session['program'] = uid['program']
                return redirect('/')
            
            elif(session['role'] == 'applicant'):
                cursor.execute("SELECT applicantID FROM applicant WHERE applicantID = %s ", (session['user_id'],))
                user_role = cursor.fetchone()
                if user_role == None:
                   return render_template('login.html', error="You selected the wrong login view")
                return redirect('/')
            
            elif(session['role'] == 'alumni'):
                cursor.execute("SELECT alumnid FROM alumni WHERE alumnid = %s ", (session['user_id'],))
                user_role = cursor.fetchone()
                if user_role == None:
                   return render_template('login.html', error="You selected the wrong login view")
                return redirect('/')
            
            elif(session['role'] == 'instructor'):
                cursor.execute("SELECT facultyID  FROM faculty WHERE facultyID = %s AND facultyRole = %s", (session['user_id'], session['role'],))
                user_role = cursor.fetchone()
                if user_role == None:
                   return render_template('login.html', error="You selected the wrong login view")
                return redirect('/')
            

            elif(session['role'] == 'gsec'):
                cursor.execute("SELECT facultyID  FROM faculty WHERE facultyID = %s AND facultyRole = %s", (session['user_id'], session['role'],))
                user_role = cursor.fetchone()
                if user_role == None:
                   return render_template('login.html', error="You selected the wrong login view")
                return redirect('/')
            
            elif(session['role'] == 'chair'):
                cursor.execute("SELECT facultyID  FROM faculty WHERE facultyID = %s AND facultyRole = %s", (session['user_id'], session['role'],))
                user_role = cursor.fetchone()
                if user_role == None:
                    return render_template('login.html', error="You selected the wrong login view")
                return redirect('/')
            
            elif(session['role'] == 'admin'):
                cursor.execute("SELECT facultyID  FROM faculty WHERE facultyID = %s AND facultyRole = %s", (session['user_id'], session['role'],))
                user_role = cursor.fetchone()
                if user_role == None:
                   return render_template('login.html', error="You selected the wrong login view")
                return redirect('/')

            elif(session['role'] == 'facultyReviewer'):
                cursor.execute("SELECT facultyID  FROM faculty WHERE facultyID = %s AND facultyRole = %s", (session['user_id'], session['role']))
                user_role = cursor.fetchone()
                return redirect('/')
        else:
            return render_template('login.html', error="You have entered an invalid username or password")
        
    return render_template("login.html")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
  session.clear()
  return redirect("/")



@app.route('/')
def index():
    
    cursor = mydb.cursor(dictionary=True)

    # check if user is logged in
    if 'uName' in session:
        username = session['uName']
        return render_template("index.html", username=username)

    return render_template("index.html")

@app.route('/profile', methods=['GET', 'POST'])
def profile():

    # check if user is logged in
    if 'uName' in session:
        role = session['role']
        
        if role == 'student':
            return redirect('/student')
        
        elif role == 'applicant':
            return redirect('/applicantHome')
        
        elif role == 'alumni':
            return redirect('/alumni')
        
        elif role == 'instructor':
            return redirect('/instructor')
        
        elif role == 'gsec':
            return redirect('/gsec')
        
        elif role == 'chair':
            return redirect('/chairHome')
        
        elif role == 'admin':
            return redirect('/admin')
        
        elif role == 'facultyReviewer':
            return redirect('/FRhome')
    
    return redirect('/')



#login and Register and Homepage--------------------------------------------------------------------------------------------------------------------------------

#student routes-------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/student')
def student():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if session['role'] != 'student':
        return redirect(url_for('logout'))
    
    if 'user_id' in session:
        cursor = mydb.cursor(dictionary=True)
        cursor2 = mydb.cursor(dictionary=True)
        cursor.execute("SELECT fname, lname FROM user WHERE uid = %s", (session['user_id'],))
        user = cursor.fetchone()

        #Get all courses
        cursor2.execute("SELECT * FROM transcript JOIN course ON transcript.cid = course.cid WHERE transcript.tuid=(%s)", (session['user_id'],))
        courses = cursor2.fetchall()

        #calculate GPA in accordance to GWU GPA policy, = sumGPA / Credit Hours
        #A, 4.0; A−, 3.7; B+, 3.3; B, 3.0; B−, 2.7; C+, 2.3; C, 2.0; C−, 1.7; and F, 0
        GPA = {
            'A':4.0,
            'A-':3.7,
            'B+':3.3,
            'B':3.0,
            'B-':2.7,
            'C+':2.3,
            'C':2.0,
            'F':0
                }
        #sum of GPA
        sumGPA = 0
        #Total of credit hours
        sumCredit = 0
        #cumalative GPA
        totalGPA = 0

        #ctr
        ctr = 0
        for course in courses:
            if course['grade'] != 'IP':
                sumGPA+= GPA[course['grade']] * course['credits']
                ctr+=1
                sumCredit+= course['credits']
        
        if ctr == 0:
            session['gpa'] = False
        else:
            totalGPA = round(sumGPA / sumCredit, 2)
            session['gpa'] = totalGPA

        cursor.execute("SELECT holding FROM form1 WHERE id = %s", (session['user_id'],))
        holding = cursor.fetchone()
        if holding is None:
            dnemsg = "You need to submit a Form1 and wait for your advisor's approval"
            ishold = None
            nohold = None
        else:
            holdings = holding['holding']
            if holdings == 1:
                ishold = "You have a registration hold, contact your advisor"
                dnemsg = None
                nohold = None
            elif holdings == 0:
                ishold = None
                dnemsg = None
                nohold = True
            else:
                ukhold = "Unknown hold status"


        if user is not None:
            return render_template('student.html', fname = user['fname'], lname = user['lname'], holding = holding, dnemsg = dnemsg, ishold = ishold, nohold = nohold)
    return redirect('/login')


@app.route('/advPortal')
def advPortal():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    isthere = False
    decisionwait = False
    cursor = mydb.cursor(dictionary=True)
    cursor2 = mydb.cursor(dictionary=True)
    if session['role'] != 'student':
        return redirect(url_for('logout'))
    
    cursor.execute(" SELECT * from thesis where uid =(%s)",(session['user_id'],))
    exists = cursor.fetchall()
    cursor2.execute(" SELECT program from student where studentid =(%s)",(session['user_id'],))
    program = cursor2.fetchone()
    masters = "masters"
    if exists:
        isthere = True
        thesis = exists[0]
        #get decision info here
        if thesis['decision'] == None:
            decisionwait = "Your thesis is under review"
        elif thesis['decision'] == 1:
            decisionwait = "Your thesis has been approved"
        elif thesis['decision'] == 0:
            decisionwait = "Your thesis has been denied"

    elif program is not None and program['program'].lower() == 'masters':
        isthere = True
        


    if 'user_id' in session:
        cursor.execute("SELECT fname FROM user WHERE uid = %s", (session['user_id'],))
        user = cursor.fetchone()
        if user is not None:
            return render_template('advPortal.html', isthere = isthere, decisionwait = decisionwait)
    return redirect('/login')

@app.route('/catalog')
def catalog():
   mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
   cursor = mydb.cursor(dictionary = True)
   cursor.execute("SELECT * FROM course ORDER by cid")
   catalog = cursor.fetchall()

   prerequisite = {}

   for course in catalog:
        cursor.execute("SELECT preqID FROM preq WHERE courseID = %s", (course['cid'],))
        prereqs = cursor.fetchall()
        prereq_list = []

        for prereq in prereqs:
            cursor.execute("SELECT dept, courseNumber FROM course WHERE cid = %s", (prereq['preqID'],))
            pre = cursor.fetchone()
            prereq_list.append(pre["dept"] + " " + str(pre["courseNumber"]))
        
        if len(prereq_list) == 0:
            prereq_list = ["None", "None"]
        elif len(prereq_list) == 1:
            prereq_list.append("None")
        prerequisite.update({course['cid']: prereq_list})

   return render_template("catalog.html", catalog = catalog, prerequisite = prerequisite)


@app.route('/registration')
def registration():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if 'user_id' in session and session['role'] == 'student':
        cursor =  mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM course ORDER BY cid")
        data = cursor.fetchall()
        return render_template("registration.html", courses = data, error = 0)
    else:
        return redirect('/')

@app.route('/schedule')
def schedule():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if 'user_id' in session and session['role'] == 'student':
        cursor =  mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM transcript INNER JOIN course ON transcript.cid = course.cid WHERE tuid = %s AND semester = %s AND year = %s ORDER BY course.cid", (session['user_id'], session['semester'], session['year']))
        data = cursor.fetchall()
        cursor.execute("SELECT DISTINCT(semester) FROM transcript WHERE tuid = %s", (session['user_id'],))
        semester = cursor.fetchall()
        cursor.execute("SELECT DISTINCT(year) FROM transcript WHERE tuid = %s", (session['user_id'],))
        years = cursor.fetchall()
        return render_template("schedule.html", courses = data, semester = semester, years = years, current_semester = session['semester'], current_year = session['year'])
    else:
        return redirect('/')

@app.route('/semester', methods=['GET', 'POST'])
def semester():
    if request.method == 'POST':
        if request.form['semester'] != "":
            session['semester'] = request.form['semester']
        if request.form['year'] != "":
            session['year'] = request.form['year']
        return redirect('/schedule')
    return redirect("/schedule")

@app.route('/add_course', methods=['GET', 'POST'])
def add():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if request.method == 'POST':
        course_id = int(request.form["course_id"])
        start = int(request.form["course_start"])
        end = int(request.form["course_end"])
        day = request.form["day"]
        cursor = mydb.cursor(dictionary = True)
        cursor.execute("SELECT * FROM course ORDER BY cid")
        data = cursor.fetchall()

        #Checks if there exists that course already in the schedule
        cursor.execute("SELECT * FROM transcript WHERE tuid = %s AND cid = %s AND semester = %s AND year = %s", (session['user_id'], course_id, session['semester'], session['year']))
        add = cursor.fetchone()

        if add != None:
            return render_template("/registration.html", courses = data, error = "You are already enrolled in this course")
        
        #Check if a PhD student signed up for classes not in 6000 level
        cursor.execute("SELECT courseNumber FROM course WHERE cid = %s", (course_id,)) 
        course_num = cursor.fetchone()
        if ((session['program'] == "PhD") and (course_num['courseNumber'] < 6000)):
            return render_template("/registration.html", courses = data, error = ("Required to register for 6000 level classes"))


        #Checks if there are prerequisite issues
        cursor.execute("SELECT preqID FROM preq WHERE courseID = %s", (course_id,))
        add = cursor.fetchall()

        for prerequisite in add:
            cursor.execute("SELECT * FROM transcript WHERE tuid = %s AND cid = %s AND grade != %s AND semester != %s AND year != %s", (session['user_id'], prerequisite['preqID'], "F", session['semester'], session['year']))
            temp = cursor.fetchall()
            if temp == []:
                error ="You have not taken one or more prerequisites: "
                for pre in add:
                    cursor.execute("SELECT * FROM course WHERE cid = %s", (pre['preqID'],))
                    temp = cursor.fetchone()
                    error = error + str(temp['dept']) + " " + str(temp['courseNumber']) + "     "
                return render_template("/registration.html", courses = data, error =  error)


        #Checks if there are schedule issues
        cursor.execute("SELECT course_start, course_end, dept, courseNumber FROM transcript INNER JOIN course ON transcript.cid = course.cid WHERE tuid = %s AND semester = %s AND year = %s AND day = %s", (session['user_id'], session['semester'], session['year'], day))
        add = cursor.fetchall()
        for course in add:
            if (course["course_start"] <= start <= course["course_end"]) or (course["course_start"] <= end <= course["course_end"]):
                return render_template("/registration.html", courses = data, error = "Scheduling conflict with existing course: " + str(course['dept']) + " " + str(course['courseNumber']))
            else:
                if start > course["course_start"]:
                    if start - course["course_end"] < 30:
                        cursor.execute("SELECT * FROM course ORDER BY cid")
                        data = cursor.fetchall()
                        return render_template("/registration.html", courses = data, error = ("Scheduling conflict with existing course: %s %s", (course['dept'], course['courseNumber'])))
                else:
                    if course["course_start"] - end < 30:
                        cursor.execute("SELECT * FROM course ORDER BY cid")
                        data = cursor.fetchall()
                        return render_template("/registration.html", courses = data, error = ("Scheduling conflict with existing course: %s %s", (course['dept'], course['courseNumber'])))

        cursor.execute("INSERT INTO transcript (tuid, cid, semester, year, grade) VALUES (%s, %s, %s, %s, %s)", (session['user_id'], course_id, session['semester'], session['year'], "IP"))
        mydb.commit()
        return redirect("/registration")
    return redirect("/registration")


@app.route('/remove_course', methods=['GET', 'POST'])
def remove_course():
  mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
  if request.method == 'POST':
    course_id = int(request.form["course_id"])
    cursor = mydb.cursor(dictionary = True)
    cursor.execute("DELETE FROM transcript WHERE tuid = %s AND cid = %s AND semester = %s AND year = %s",(session['user_id'], course_id, session['semester'], session['year']))
    mydb.commit()
  return redirect('/schedule')

@app.route('/form', methods=['GET', 'POST'])
def form():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    message = ""

    cursor = mydb.cursor(dictionary=True)

    if request.method == 'POST':
        # check if student id exists in students table
        cursor.execute("SELECT * FROM student WHERE studentid=%s", (session['user_id'],))
        student = cursor.fetchone()

        if student:
            # retrieve course data from form fields
            courses = []
            for i in range(1, 13):
                courseDept = request.form.get(f"class{i}dept")
                courseNum = request.form.get(f"class{i}num")
                if courseDept and courseNum:
                    courses.append((courseDept.upper()[:4], courseNum))

            if courses:
                # insert form data into form1 table
                sql = "INSERT INTO form1 (id, courseDept, courseNum, holding) VALUES (%s, %s, %s, 1)"
                values = [(session['user_id'], course[0], course[1]) for course in courses]
                cursor.executemany(sql, values)
                mydb.commit()

                message = "Form submitted successfully!"
            else:
                message = "Please enter at least one course"
        else:
            message = "Invalid student ID"

    return render_template('form.html', message=message)




@app.route('/graduating')
def graduating():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    
    cursor = mydb.cursor(dictionary=True)
    
    if session['role'] != "student":
        return redirect(url_for('logout'))
    
    #Create course list before they submit
    cursor.execute("SELECT * FROM transcript JOIN course ON transcript.cid = course.cid WHERE transcript.tuid=(%s)", (session['user_id'],))
    
    courses = cursor.fetchall()


    return render_template('graduating.html', courses = courses)




@app.route('/transcript_student')
def transcript4students():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if session['role'] != "student":
        return redirect(url_for('logout'))
    
    cursor = mydb.cursor(dictionary = True)

    if not session['user_id']:
        return redirect(url_for('index'))
    
    #Get all courses, sort by date
    cursor.execute("SELECT * FROM transcript JOIN course ON transcript.cid = course.cid WHERE transcript.tuid=(%s) ORDER BY transcript.year ASC", (session['user_id'],))
    transcript = cursor.fetchall()
        #calculate GPA in accordance to GWU GPA policy, = sumGPA / Credit Hours
        #A, 4.0; A−, 3.7; B+, 3.3; B, 3.0; B−, 2.7; C+, 2.3; C, 2.0; C−, 1.7; and F, 0
    GPA = {
        'A':4.0,
        'A-':3.7,
        'B+':3.3,
        'B':3.0,
        'B-':2.7,
        'C+':2.3,
        'C':2.0,
        'F':0
            }
    #sum of GPA
    sumGPA = 0
    #Total of credit hours
    sumCredit = 0
    #cumalative GPA
    totalGPA = 0

    #ctr
    ctr = 0
    for trans in transcript:
        if trans['grade'] != 'IP':
            sumGPA+= GPA[trans['grade']] * trans['credits']
            ctr+=1
            sumCredit+= trans['credits']
    
    if ctr == 0:
        session['gpa'] = False
    else:
        totalGPA = round(sumGPA / sumCredit, 2)
        session['gpa'] = totalGPA
    
    if session['gpa'] != False:
        gpa = session['gpa']
    else:
        gpa = "You have no transcript"

    return render_template("transcript.html", transcript = transcript, gpa = gpa)




@app.route('/apply2grad')
def apply2grad():  
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor = mydb.cursor(dictionary=True)
    message = " "
    
    if session['role'] != "student":
        return redirect(url_for('logout'))
    
    #Get all courses
    cursor.execute("SELECT * FROM transcript JOIN course ON transcript.cid = course.cid WHERE transcript.tuid=(%s)", (session['user_id'],))
    
    courses = cursor.fetchall()
    mydb.commit()
    #see if they are masters or phd
    cursor.execute("SELECT * FROM student WHERE studentid=(%s)",(session['user_id'],))
    user = cursor.fetchone()
    programName = user['program']
    #calculate GPA in accordance to GWU GPA policy, = sumGPA / Credit Hours
    #A, 4.0; A−, 3.7; B+, 3.3; B, 3.0; B−, 2.7; C+, 2.3; C, 2.0; C−, 1.7; and F, 0
    GPA = {
        'A':4.0,
        'A-':3.7,
        'B+':3.3,
        'B':3.0,
        'B-':2.7,
        'C+':2.3,
        'C':2.0,
        'F':0
            }
    #sum of GPA
    sumGPA = 0
    #Total of credit hours
    sumCredit = 0
    #cumalative GPA
    totalGPA = 0

    #ctr
    ctr = 0
    belowBcounter = 0
    for course in courses:
        if course['grade'] != 'IP':
            sumGPA+= GPA[course['grade']] * course['credits']
            ctr+=1
            if GPA[course['grade']] < 3:
                belowBcounter += 1
            sumCredit+= course['credits']
            
    if ctr < 1:
        message = "You have not completed any courses yet!"
        return render_template("graduating.html", courses = courses, message = message )

    totalGPA = round(sumGPA / sumCredit, 2)
    
    canthisgraduatestudentgraduate = False
    OutsideCS = 0

    if programName == 'masters':
        #If Total GPA is above or equal to 3 and total credits is more than 30 
        #no more than two grades below a B, then see if they completed all the req class
        if belowBcounter >= 3:
            message = "You are currently under academic suspension"
            return render_template("graduating.html", courses = courses, message = message)
        
        if totalGPA >= 3.0 and sumCredit >= 30 and belowBcounter<=2:
            CSCI6212 = False
            CSCI6221 = False
            CSCI6461 = False
            
            for course in courses:
                if course['courseNumber'] == 6212:
                    CSCI6212 = True
                if course['courseNumber'] == 6221:
                    CSCI6221 = True
                if course['courseNumber'] == 6461:
                    CSCI6461 = True                    
                if course['dept'] != 'CSCI':
                    OutsideCS += 1
            #If they have taken all the courses needed and at most 2 out of CSCI
            if CSCI6461 and CSCI6221 and CSCI6212 and OutsideCS<=2:
                canthisgraduatestudentgraduate = True

        if canthisgraduatestudentgraduate == False and totalGPA < 3:
            flash('You are not eligible to graduate because your gpa is too low')
        
        if canthisgraduatestudentgraduate == False and sumCredit < 30:
            flash('You are not eligible to graduate because you dont have enough credits')
        
        if canthisgraduatestudentgraduate == False and belowBcounter > 2:
            flash('You are not eligible to graduate because you have recieved the grade b too many times')
    

    if programName == 'phd':
        cursor.execute("SELECT decision FROM thesis WHERE uid=(%s)", (session['user_id'],))
        decision = cursor.fetchone()
        if decision['decision'] == 1:
            Finaldecision = True
        else:
            Finaldecision = False


        if belowBcounter >= 3:
            message = "You are currently under academic suspension"
            return render_template("graduating.html", courses = courses, message = message)
        #Total GPA 3.5 or higher, 36 credit hours
        if totalGPA >= 3.5 and sumCredit >= 36 and belowBcounter <= 1 and Finaldecision == True:
            
            for course in courses:
                if course['dept'] == 'CSCI':
                    #OutsideCS in this case is actually courses in CS but im lazy
                    OutsideCS += course['credits']
            if OutsideCS >= 30:
                canthisgraduatestudentgraduate = True
                
        if canthisgraduatestudentgraduate == False and totalGPA < 3.5:
            flash('You are not eligible to graduate because your gpa is too low, contact your advisor')
        
        if canthisgraduatestudentgraduate == False and sumCredit < 36:
            flash('You are not eligible to graduate because you dont have enough credits, contact your advisor')
        
        if canthisgraduatestudentgraduate == False and belowBcounter > 1:
            flash('You are not eligible to graduate because you have recieved the grade b too many times ')

        if canthisgraduatestudentgraduate == False and Finaldecision == False:
            flash('You are not eligible to graduate because your thesis decision has not been approved, contact your advisor')
    
    if canthisgraduatestudentgraduate == True:
        cursor.execute("UPDATE student SET rdygrad = 1 WHERE studentid = (%s)",(session['user_id'],))
        flash('You have sucessfully applied to graduate! Wait for graduate secretary approval')
        mydb.commit()
        
    

        return redirect(url_for('graduating'))
    return redirect(url_for('graduating'))

@app.route('/studentUpdate', methods=['GET', 'POST'])
def studentUpdate():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if session['role'] != "student":
        return redirect(url_for('logout'))
    
    cursor = mydb.cursor(dictionary=True)
    
    if 'username' in session:
        uName = session['username']
    else:
        uName = None
    
    # Check if uname is in student
    cursor.execute("SELECT * FROM user WHERE uid=(%s)", (session['user_id'],))
    student_user = cursor.fetchone()

    if student_user:

        if request.method == 'POST':
            # Update student information in the database
            new_email = request.form['email']
            new_addy = request.form['address']
            cursor.execute("UPDATE user SET email=(%s), address=(%s) WHERE uid=(%s)", (new_email, new_addy, session['user_id'],))
            mydb.commit()

        # Fetch alumni data for the signed in user
        cursor.execute("SELECT * FROM user WHERE uid=(%s)", (session['user_id'],))
        student_data = cursor.fetchone()

        if not student_data:
            return redirect(url_for('index'))
        
    return render_template('studentUpdate.html', student_data=student_data, username=uName)


#users can write duplicates**************************
@app.route('/writeThesis', methods=['GET', 'POST'])
def writeThesis():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if session['role'] != "student":
        return redirect(url_for('logout'))

    cursor = mydb.cursor(dictionary=True)
    if 'user_id' in session:
        if request.method == 'POST':
            thesis = request.form['thesis']
            uid = session['user_id']
            decision = None
            cursor.execute("INSERT INTO thesis (thesis, uid, decision) VALUES (%s, %s, %s)", (thesis, uid, decision))
            mydb.commit()
            flash("Thesis submitted successfully!", "success")
            return redirect(url_for('writeThesis'))
        return render_template("studenthesis.html")
    return render_template("studenthesis.html")




#student routes-------------------------------------------------------------------------------------------------------------------------------------------------

#gsec routes----------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/gsec')
def gsec():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if session['role'] != "gsec":
        return redirect(url_for('logout'))
    
    if 'user_id' in session:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT fname,lname FROM user WHERE uid = %s", (session['user_id'],))
        user = cursor.fetchone()
        if user is not None:
            return render_template('GSHome.html', fname=user['fname'], lname=user['lname'])
    return redirect(url_for('login'))

@app.route('/gsecadv')
def gsecadv():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if session['role'] != "gsec":
        return redirect(url_for('logout'))

    if 'user_id' in session:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT fname, lname FROM user WHERE uid = %s", (session['user_id'],))
        user = cursor.fetchone()
        if user is not None:
            cursor.execute("SELECT user.fname, user.lname, student.studentid, student.program, student.rdygrad FROM user LEFT JOIN student ON user.uid = student.studentid WHERE student.rdygrad = 1")
            students = cursor.fetchall()
            return render_template('gsecadvportal.html', students=students)
    return redirect('/login')


@app.route('/chairUpdateStatus', methods=['GET', 'POST'])
def chairUpdateStatus():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor = mydb.cursor(dictionary = True)
    if request.method == 'POST':
        job = request.form["status"]
        studentid = request.form["id"]


        cursor.execute("SELECT degreeSeeking FROM ApplicationForm WHERE studentID = %s", (studentid,))
        pname = cursor.fetchone()
        if pname != None:
            program = pname['degreeSeeking']


        if job == 'Admission Decision: Accepted':
            # Insert the student's information into the alumni table
            cursor.execute("INSERT INTO student (studentid, program, rdygrad, advisorid) VALUES ((%s),(%s),(%s),(%s))", (studentid, program, 0, None))
            mydb.commit()
            # Delete the student's information from the students table
            cursor.execute("DELETE FROM applicant WHERE applicantID = (%s)", (studentid,))
            mydb.commit()
            cursor.execute("SELECT user.username, user.UID, applicant.applicantStatus FROM user INNER JOIN applicant ON user.UID = applicant.applicantID")
            applicants = cursor.fetchall()
            for applicant in applicants:
                if applicant['applicantStatus'] == 'Application Materials Missing':
                    applicant['display'] = False
                else:
                    applicant['display'] = True
            if applicants != None:
                msg = "succesfully admitted a student!"
                return render_template("chairHome.html", applicants = applicants, msg =msg)
            else:
                nomore = "There are no more applicants to review"
                return render_template("chairHome.html", nomore =nomore)


        if job == 'Admission Decision: Reject':
            # Insert the student's information into the alumni table
            cursor.execute("DELETE FROM user WHERE UID = %s", (studentid,))
            mydb.commit()
            # Delete the student's information from the students table
            cursor.execute("DELETE FROM applicant WHERE applicantID = (%s)", (studentid,))
            mydb.commit()
            cursor.execute("SELECT user.username, user.UID, applicant.applicantStatus FROM user INNER JOIN applicant ON user.UID = applicant.applicantID")
            applicants = cursor.fetchall()
            for applicant in applicants:
                if applicant['applicantStatus'] == 'Application Materials Missing':
                    applicant['display'] = False
                else:
                    applicant['display'] = True
            if applicants != None:
                msg = "succesfully denied a student >:("
                return render_template("chairHome.html", applicants = applicants, msg =msg)
            else:
                nomore = "There are no more applicants to review"
                return render_template("chairHome.html", nomore =nomore)

        else:
            cursor.execute("UPDATE applicant SET applicantStatus = (%s) WHERE applicantID = (%s)", (job, studentid,))
            mydb.commit()
            cursor.execute("SELECT user.username, user.UID, applicant.applicantStatus FROM user INNER JOIN applicant ON user.UID = applicant.applicantID")
            applicants = cursor.fetchall()
            for applicant in applicants:
                if applicant['applicantStatus'] == 'Application Materials Missing':
                    applicant['display'] = False
                else:
                    applicant['display'] = True
            msg = "succesfully updated applicant status"
            return render_template("chairHome.html", applicants = applicants, msg =msg)
    return render_template("chairHome.html", applicants = applicants)

@app.route('/listofapps', methods=['GET', 'POST'])
def listofapps():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor = mydb.cursor(dictionary = True)
    cursor.execute("SELECT user.username, user.UID, applicant.applicantStatus FROM user INNER JOIN applicant ON user.UID = applicant.applicantID")
    applicants = cursor.fetchall()
    for applicant in applicants:
        if applicant['applicantStatus'] == 'Application Materials Missing':
            applicant['display'] = False
        else:
            applicant['display'] = True
    return render_template("gsapps.html", applicants=applicants)

@app.route('/search', methods = ['GET', 'POST'])
def search():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor = mydb.cursor(dictionary = True)
    if request.method == 'POST':
        name = request.form["search"]
        nameString = '%' + name + '%'
        cursor.execute("SELECT user.username, user.UID, applicant.applicantStatus FROM user INNER JOIN applicant ON user.UID = applicant.applicantID WHERE user.username = %s ", (nameString,))
        applicants = cursor.fetchall()
        return render_template("gsapps.html", applicants=applicants)

    cursor.execute("SELECT user.username, user.UID, applicant.applicantStatus FROM user INNER JOIN applicant ON user.UID = applicant.applicantID")
    applicants = cursor.fetchall()
    return render_template("gsapps.html", applicants=applicants)

@app.route('/gsapps', methods=['GET', 'POST'])
def gsapps():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor = mydb.cursor(dictionary = True)
    if session['role'] != "gsec":
        return redirect(url_for('logout'))
    
    if request.method == 'POST': 
        if request.form["type"] == "update":
            job = request.form["status"]
            studentid = request.form["id"]


            cursor.execute("SELECT degreeSeeking FROM ApplicationForm WHERE studentID = %s", (studentid,))
            pname = cursor.fetchone()
            if pname != None:
                program = pname['degreeSeeking']


            if job == 'Admission Decision: Accepted':
                # Insert the student's information into the alumni table
                cursor.execute("INSERT INTO student (studentid, program, rdygrad, advisorid) VALUES ((%s),(%s),(%s),(%s))", (studentid, program, 0, None))
                mydb.commit()
                # Delete the student's information from the students table
                cursor.execute("DELETE FROM applicant WHERE applicantID = (%s)", (studentid,))
                mydb.commit()
                cursor.execute("SELECT user.username, user.UID, applicant.applicantStatus FROM user INNER JOIN applicant ON user.UID = applicant.applicantID")
                applicants = cursor.fetchall()
                for applicant in applicants:
                    if applicant['applicantStatus'] == 'Application Materials Missing':
                        applicant['display'] = False
                    else:
                        applicant['display'] = True
                if applicants != None:
                    msg = "succesfully admitted a student!"
                    return render_template("gsapps.html", applicants = applicants, msg =msg)
                else:
                    nomore = "There are no more applicants to review"
                    return render_template("gsapps.html", nomore =nomore)


            if job == 'Admission Decision: Reject':
                # Insert the student's information into the alumni table
                cursor.execute("DELETE FROM user WHERE UID = %s", (studentid,))
                mydb.commit()
                # Delete the student's information from the students table
                cursor.execute("DELETE FROM applicant WHERE applicantID = (%s)", (studentid,))
                mydb.commit()
                cursor.execute("SELECT user.username, user.UID, applicant.applicantStatus FROM user INNER JOIN applicant ON user.UID = applicant.applicantID")
                applicants = cursor.fetchall()
                for applicant in applicants:
                    if applicant['applicantStatus'] == 'Application Materials Missing':
                        applicant['display'] = False
                    else:
                        applicant['display'] = True
                if applicants != None:
                    msg = "succesfully denied a student >:("
                    return render_template("gsapps.html", applicants = applicants, msg =msg)
                else:
                    nomore = "There are no more applicants to review"
                    return render_template("gsapps.html", nomore =nomore)

            else:
                cursor.execute("UPDATE applicant SET applicantStatus = (%s) WHERE applicantID = (%s)", (job, studentid,))
                mydb.commit()
                cursor.execute("SELECT user.username, user.UID, applicant.applicantStatus FROM user INNER JOIN applicant ON user.UID = applicant.applicantID")
                applicants = cursor.fetchall()
                for applicant in applicants:
                    if applicant['applicantStatus'] == 'Application Materials Missing':
                        applicant['display'] = False
                    else:
                        applicant['display'] = True
                msg = "succesfully updated applicant status"
                return render_template("gsapps.html", applicants = applicants, msg =msg)
            
        if request.form["type"] == "app":
            cursor.execute("SELECT * FROM ApplicationForm WHERE studentID = %s", (request.form["id"],))
            app = cursor.fetchone()
            id = request.form["id"]
            return render_template("GSseeApplications.html", app=app, id=id)

        if request.form["type"] == "review":
            cursor.execute("SELECT * FROM ReviewForm WHERE studentID = %s", (request.form["id"],))
            form = cursor.fetchone()
            id = request.form["id"]
            return render_template("GSseeReviews.html", form=form, id=id)

    cursor.execute("SELECT * FROM applicant")
    applicants = cursor.fetchall()

    return render_template("gsapps.html", applicants=applicants)
    
    
@app.route('/GSupdateapp', methods=['GET','POST'])
def GSupdateapp():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor = mydb.cursor(dictionary = True)

    if request.method == 'POST':
        if request.form["type"] == "transcript":
            cursor.execute("UPDATE ApplicationForm SET transcriptStatus = %s WHERE studentID = %s", ("Transcript Recieved",request.form["id"]))
            mydb.commit()

        if request.form["type"] == "r1":
            cursor.execute("UPDATE applicationForm SET r1status = %s WHERE studentID = %s", ("Rec Letter 1 Recieved",request.form["id"]))
            mydb.commit()

        if request.form["type"] == "r2":
            cursor.execute("UPDATE applicationForm SET r2status = %s WHERE studentID = %s", ("Rec Letter 2 Recieved",request.form["id"]))
            mydb.commit()

        if request.form["type"] == "r3":
            cursor.execute("UPDATE applicationForm SET r3status = %s WHERE studentID = %s", ("Rec Letter 3 Recieved",request.form["id"]))
            mydb.commit()

    cursor.execute("SELECT * FROM applicationForm WHERE studentID = %s", (request.form["id"],))
    app = cursor.fetchone()

    id = request.form["id"]

    return render_template("GSseeApplications.html", app=app, id=id)


@app.route('/gsecgradbtn/<int:uid>', methods=['POST'])
def gsecgradbtn(uid):
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor = mydb.cursor(dictionary=True)

    # Get the student's information from the students table
    cursor.execute("SELECT * FROM student WHERE studentid = %s", (uid,))
    student = cursor.fetchone()

    if student:
        # Check if the alumni record already exists
        cursor.execute("SELECT * FROM alumni WHERE alumnid = %s", (uid,))
        alumni = cursor.fetchone()

        if not alumni:
            # Insert the student's information into the alumni table
            cursor.execute("INSERT INTO alumni (alumnid) VALUES (%s)", (uid,))
            mydb.commit()
            # Delete the student's information from the students table
            cursor.execute("DELETE FROM student WHERE studentid = %s", (uid,))
            mydb.commit()
    
    return redirect(url_for('gsec'))



@app.route('/adminViewForm', methods=['GET', 'POST'])
def adminViewForm():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor = mydb.cursor(dictionary=True)
    cursor2 = mydb.cursor(dictionary=True)
    cursor3 = mydb.cursor(dictionary=True)

    if session['role'] != "admin" and session['role'] != "gsec":
        return redirect(url_for('logout'))
    
    if 'user_id' in session:
        cursor.execute("SELECT DISTINCT uid, fname, lname FROM user INNER JOIN student ON student.studentid = user.uid INNER JOIN form1 ON form1.id = student.studentid where form1.holding = 1")
        students = cursor.fetchall()

    if request.method == 'POST':
        studentId = request.form['field_id']

        cursor2.execute("SELECT fname, lname FROM user WHERE uid = (%s) ", (studentId,))
        row = cursor.fetchone()
        studentName = row['fname']


        cursor3.execute("SELECT id, courseDept, courseNum FROM form1 WHERE id = (%s)", (studentId,))
        results = cursor3.fetchall()
        mydb.commit()

        return render_template('adminViewform.html', results = results, name = studentName, students = students)

    return render_template('adminViewForm.html', students=students)

@app.route('/adminform_approve', methods = ['GET', 'POST'])
def adminform_approve():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor = mydb.cursor(dictionary=True)

    if session['role'] != "admin" and session['role'] != "gsec":
        return redirect(url_for('logout'))
    
    if request.method == 'POST':
        studentId = request.form['field_id']
        if request.form['y/n'] == "yes":
            cursor.execute("UPDATE form1 SET holding = (%s) WHERE id=(%s)",(0, studentId,))
            mydb.commit()
        else:
            cursor.execute("UPDATE form1 SET holding = (%s) WHERE id=(%s)",(0, studentId,))
            mydb.commit()
    return redirect(url_for('adminViewForm'))



@app.route('/adminViewTrans', methods = ['GET','POST'])
def adminViewTrans():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor = mydb.cursor(dictionary=True)
    cursor2 = mydb.cursor(dictionary=True)
    cursor3 = mydb.cursor(dictionary=True)
    cursor4 = mydb.cursor(dictionary=True)
    if session['role'] != "admin"  and session['role'] != "gsec":
        return redirect(url_for('logout'))
    if 'user_id' in session:
        cursor.execute("SELECT DISTINCT uid, fname, lname FROM user INNER JOIN student ON student.studentid = user.uid INNER JOIN transcript ON transcript.tuid = student.studentid;")
        students = cursor.fetchall()

        if request.method == 'POST':
            studentId = request.form['field_id']

            cursor2.execute("SELECT fname, lname FROM user WHERE uid = (%s) ", (studentId,))
            row = cursor2.fetchone()
            studentName = row['fname']


            cursor3.execute("SELECT * FROM transcript JOIN course ON transcript.cid = course.cid WHERE transcript.tuid=(%s) ORDER BY transcript.year ASC", (studentId,))
            transcript = cursor3.fetchall()

            #Get all courses
            cursor4.execute("SELECT * FROM transcript JOIN course ON transcript.cid = course.cid WHERE transcript.tuid=(%s)", (studentId,))
            courses = cursor4.fetchall()

            #calculate GPA in accordance to GWU GPA policy, = sumGPA / Credit Hours
            #A, 4.0; A−, 3.7; B+, 3.3; B, 3.0; B−, 2.7; C+, 2.3; C, 2.0; C−, 1.7; and F, 0
            GPA = {
            'A':4.0,
            'A-':3.7,
            'B+':3.3,
            'B':3.0,
            'B-':2.7,
            'C+':2.3,
            'C':2.0,
            'F':0
                }
            #sum of GPA
            sumGPA = 0
            #Total of credit hours
            sumCredit = 0
            #cumalative GPA
            totalGPA = 0

            #ctr
            ctr = 0
            belowBcounter = 0
            for course in courses:
                if course['grade'] != 'IP':
                    sumGPA+= GPA[course['grade']] * course['credits']
                    ctr+=1
                    sumCredit+= course['credits']
            
            if ctr == 0:
                totalGPA = False
            else:
                totalGPA = round(sumGPA / sumCredit, 2)

            if totalGPA!= False:
                gpa = totalGPA
            
            
            return render_template('adminTranscript.html', transcript = transcript, name = studentName, students = students, gpa = gpa)

        return render_template('adminTranscript.html', students = students)
    return redirect('/')


#needs work
@app.route('/assign', methods = ['GET', 'POST'])
def assign():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if session['role'] != "admin"  and session['role'] != "gsec":
        return redirect(url_for('logout'))
    message = " "

    cursor = mydb.cursor(dictionary=True)
    cursor2 = mydb.cursor(dictionary=True)

    cursor.execute("SELECT studentid FROM student")
    students = cursor.fetchall()

    cursor2.execute("SELECT facultyid FROM faculty WHERE facultyRole = (%s)", ("instructor",))
    facultys = cursor2.fetchall()
    
    if request.method == 'POST':
        advisorId = request.form['field_advId']
        studentId = request.form['field_stuId']

        cursor.execute('UPDATE student SET advisorid = (%s) WHERE studentid = (%s)', (advisorId, studentId,))
        message = "Succesfully Assigned"
        mydb.commit()
        return render_template('assign.html', students = students, facultys = facultys, message = message)
    return render_template('assign.html',students = students, facultys = facultys)



@app.route('/viewAllStudents', methods = ['GET', 'POST'])
def viewAllStudents():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor = mydb.cursor(dictionary=True)
    cursor2 = mydb.cursor(dictionary=True)

    if session['role'] != "gsec" and session['role'] != "admin":
        return redirect(url_for('logout'))

    if session['role'] == "gsec" or session['role'] == "admin":

        cursor.execute('SELECT studentid FROM student ORDER BY studentid ASC')
        studentids = [row['studentid'] for row in cursor.fetchall()]
        results = []
        for studentid in studentids:
            cursor2.execute('SELECT * FROM user WHERE uid = (%s)', (studentid,))
            student_info = cursor2.fetchone()
            if student_info:
                results.append(student_info)
        
        return render_template('viewAllStudents.html', results=results)
    return render_template('viewAllStudents.html')
#gsec routes^---------------------------------------------------------------------------------------------------------------------------------------------------------



#instructor routes----------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/instructor')
def instructor():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if session['role'] != "instructor":
        return redirect(url_for('logout'))
    if 'user_id' in session:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT fname, lname FROM user WHERE uid = %s", (session['user_id'],))
        user = cursor.fetchone()
        cursor.execute("SELECT studentid FROM student WHERE advisorid = %s", (session['user_id'],))
        advised = cursor.fetchall()
        if user and advised is not None:
            return render_template('instructor.html', fname=user['fname'], lname=user['lname'], advised = advised)
    return redirect('/login')

@app.route('/adv')
def adv():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if session['role'] != "instructor":
        return redirect(url_for('logout'))

    if 'user_id' in session:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT fname, lname FROM user WHERE uid = %s", (session['user_id'],))
        username = cursor.fetchone()
        if username is not None:
            return render_template('advisor.html', username = username)
    return redirect('/login')

@app.route('/grade_course', methods=['GET', 'POST'])
def grade_course():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor =  mydb.cursor(dictionary=True)
    if session['role'] != "instructor" and session['role'] != "gsec":
        return redirect('/')

    if request.method == 'POST':
        course_id = request.form["course_id"]
        cursor.execute("SELECT * FROM course WHERE cid = %s",(course_id,))
        course = cursor.fetchone()

        cursor.execute("SELECT * FROM transcript INNER JOIN student ON student.studentid = transcript.tuid INNER JOIN user ON user.uid = student.studentid WHERE transcript.cid = %s AND transcript.semester = %s AND transcript.year = %s",(course_id, "Spring", "2023"))
        students = cursor.fetchall()

        return render_template("grade_student.html", students = students, course = course)

    if session['role'] == "instructor":
        cursor.execute("SELECT * FROM course WHERE instructorID = %s", (session['user_id'],))
    elif session['role'] == "gsec":
        cursor.execute("SELECT * FROM course")
    data = cursor.fetchall()

    return render_template("grade_course.html", courses = data)

@app.route('/grade_edit', methods=['GET', 'POST'])
def grade_edit():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if request.method == 'POST':
        # implement the update to the database for the grade change
        cursor =  mydb.cursor(dictionary=True)

        student_id = request.form["student_id"]
        course_id = request.form["course_id"]
        grade = request.form["grade"]

        cursor.execute("SELECT grade FROM transcript WHERE tuid = %s AND cid = %s AND semester = %s AND year = %s",(student_id, course_id, "Spring", "2023"))
        current_grade = cursor.fetchone()

        possible_grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'F']
        # checking to make sure that a valid grade is given

        if grade in possible_grades and ((session['role'] == "instructor" and current_grade['grade'] == "IP") or (session['role'] == "gsec")):
            cursor.execute("UPDATE transcript SET grade = %s WHERE tuid = %s AND cid = %s AND semester = %s AND year = %s", (grade, student_id, course_id, "Spring", "2023"))
            mydb.commit()

        cursor.execute("SELECT * FROM course WHERE cid = %s",(course_id,))
        course = cursor.fetchone()

        cursor.execute("SELECT * FROM transcript INNER JOIN student ON student.studentid = transcript.tuid INNER JOIN user ON user.uid = student.studentid WHERE transcript.cid = %s AND transcript.semester = %s AND transcript.year = %s",(course_id, "Spring", "2023"))
        students = cursor.fetchall()

        return render_template("grade_student.html", students = students, course = course)
    
    return redirect('/gs-view')

@app.route('/viewAdvisedStudent')
def viewAdvised():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if session['role'] != "instructor" and session['role'] != "gsec" and session['role'] != "admin":
        return redirect(url_for('logout'))
    
    cursor = mydb.cursor(dictionary=True)
    cursor2 = mydb.cursor(dictionary=True)

    if session['role'] == "instructor": 
        seshrole = False
        cursor.execute('SELECT studentid FROM student WHERE advisorId = (%s)', (session['user_id'],))
        studentids = [row['studentid'] for row in cursor.fetchall()]
        results = []
        for studentid in studentids:
            cursor2.execute('SELECT * FROM user WHERE uid = (%s)', (studentid,))
            student_info = cursor2.fetchone()
            if student_info:
                results.append(student_info)
          
        return render_template('viewAdvised.html', results=results, seshrole = seshrole, user_id = session['user_id'])
    
    if session['role'] == "gsec" or session['role'] == "admin":
        seshrole = True
        cursor.execute('SELECT studentid FROM student WHERE advisorid IS NOT NULL')
        studentids = [row['studentid'] for row in cursor.fetchall()]
        results = []
        for studentid in studentids:
            cursor2.execute('SELECT * FROM user WHERE uid = (%s)', (studentid,))
            student_info = cursor2.fetchone()
            cursor2.execute('SELECT advisorid FROM student WHERE studentid = (%s)', (studentid,))
            advisor_info = cursor2.fetchone()

            if student_info:
                student_info['advisorid'] = advisor_info['advisorid']
                results.append(student_info)
          
        return render_template('viewAdvised.html', results=results, seshrole = seshrole)


    return render_template('viewAdvised.html')
    




@app.route('/viewForm', methods = ['GET','POST'])
def viewForm():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    message = " "
    error = False 
    cursor = mydb.cursor(dictionary=True)
    cursor2 = mydb.cursor(dictionary=True)
    cursor3 = mydb.cursor(dictionary=True)

    if session['role'] != "instructor":
        return redirect(url_for('logout'))
    
    if 'user_id' in session:
        cursor.execute("SELECT DISTINCT uid, fname, lname FROM user INNER JOIN student ON student.studentid = user.uid INNER JOIN form1 ON form1.id = student.studentid where student.advisorid = %s AND form1.holding = 1", (session['user_id'],))
        students = cursor.fetchall()

    if request.method == 'POST':
        studentId = request.form['field_id']

        cursor2.execute("SELECT fname, lname FROM user WHERE uid = (%s) ", (studentId,))
        row = cursor2.fetchone()
        studentName = row['fname']


        cursor3.execute("SELECT id, courseDept, courseNum FROM form1 WHERE id = (%s)", (studentId,))
        results = cursor3.fetchall()
        mydb.commit()

        return render_template('viewform.html', results = results, name = studentName, students = students)

    return render_template('viewForm.html', students=students)

@app.route('/form_approve', methods = ['GET', 'POST'])
def form_approve():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor = mydb.cursor(dictionary=True)

    if session['role'] != "instructor":
        return redirect(url_for('logout'))
    
    if request.method == 'POST':
        studentId = request.form['field_id']
        if request.form['y/n'] == "yes":
            cursor.execute("UPDATE form1 SET holding = (%s) WHERE id=(%s)",(0, studentId,))
            mydb.commit()
        else:
            cursor.execute("UPDATE form1 SET holding = (%s) WHERE id=(%s)",(0, studentId,))
            mydb.commit()
    return redirect(url_for('viewForm'))
        



@app.route('/thesis', methods = ['GET', 'POST'])
def thesis():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor = mydb.cursor(dictionary=True)
    if session['role'] != "instructor" and session['role'] != "admin":
        return redirect(url_for('logout'))
    
    #if instructor
    if session['role'] == "instructor":
        #For the  select
        cursor.execute("SELECT DISTINCT user.uid, user.fname, user.lname FROM user INNER JOIN student ON student.studentid = user.uid INNER JOIN thesis ON thesis.uid = student.studentid WHERE student.advisorid =(%s)",(session['user_id'],))
        students = cursor.fetchall()

    #if admin
    elif session['role'] == "admin":
        #For all
        cursor.execute("SELECT DISTINCT uid, fname, lname FROM user INNER JOIN student ON student.studentid = user.uid INNER JOIN thesis ON thesis.uid = student.studentid;")
        students = cursor.fetchall()

    #If post select specific student and display
    if request.method == 'POST':
        cursor.execute("SELECT * FROM thesis JOIN student ON thesis.uid = student.studentid WHERE thesis.uid=(%s)",(request.form["field_id"],))
        thesis = cursor.fetchall()
        if thesis:
            decision = thesis[0]['decision']
        else:
            decision = None

        return render_template('thesis.html', students = students, thesis=thesis, decision = decision)
    return render_template('thesis.html', students=students)



@app.route('/thesis_approve', methods = ['GET', 'POST'])
def thesis_approve():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor = mydb.cursor(dictionary=True)

    if session['role'] != "instructor" and session['role'] != "admin":
        return redirect(url_for('logout'))
    
    if request.method == 'POST':
        if request.form['y/n'] == "yes":
            cursor.execute("UPDATE thesis SET thesis.decision = 1 WHERE uid=(%s)",(request.form['uid'],))
            mydb.commit()
        elif request.form['y/n'] == "ur":
            cursor.execute("UPDATE thesis SET thesis.decision = NULL WHERE uid=(%s)",(request.form['uid'],))
            mydb.commit()
        else:
            cursor.execute("UPDATE thesis SET thesis.decision = 0 WHERE uid=(%s)",(request.form['uid'],))
            mydb.commit()
    return redirect(url_for('thesis'))



@app.route('/transcript_advisor', methods = ['GET', 'POST'])
def transcript4advisor():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if session['role'] != "instructor":
        return redirect(url_for('logout'))

    cursor = mydb.cursor(dictionary=True)
    cursor2 = mydb.cursor(dictionary=True)
    cursor3 = mydb.cursor(dictionary=True)
    cursor4 = mydb.cursor(dictionary=True)

    if 'user_id' in session:
        cursor.execute("SELECT DISTINCT uid, fname, lname FROM user INNER JOIN student ON student.studentid = user.uid INNER JOIN transcript ON transcript.tuid = student.studentid where student.advisorid = %s ", (session['user_id'],))
        students = cursor.fetchall()

        if request.method == 'POST':
            studentId = request.form['field_id']

            cursor2.execute("SELECT fname, lname FROM user WHERE uid = (%s) ", (studentId,))
            row = cursor2.fetchone()
            studentName = row['fname']


            cursor3.execute("SELECT * FROM transcript JOIN course ON transcript.cid = course.cid WHERE transcript.tuid=(%s) ORDER BY transcript.year ASC", (studentId,))
            transcript = cursor3.fetchall()

            #Get all courses
            cursor4.execute("SELECT * FROM transcript JOIN course ON transcript.cid = course.cid WHERE transcript.tuid=(%s)", (studentId,))
            courses = cursor4.fetchall()

            #calculate GPA in accordance to GWU GPA policy, = sumGPA / Credit Hours
            #A, 4.0; A−, 3.7; B+, 3.3; B, 3.0; B−, 2.7; C+, 2.3; C, 2.0; C−, 1.7; and F, 0
            GPA = {
                'A':4.0,
                'A-':3.7,
                'B+':3.3,
                'B':3.0,
                'B-':2.7,
                'C+':2.3,
                'C':2.0,
                'F':0
                    }
            #sum of GPA
            sumGPA = 0
            #Total of credit hours
            sumCredit = 0
            #cumalative GPA
            totalGPA = 0

            #ctr
            ctr = 0
            belowBcounter = 0
            for course in courses:
                if course['grade'] != 'IP':
                    sumGPA+= GPA[course['grade']] * course['credits']
                    ctr+=1
                    sumCredit+= course['credits']
            
            if ctr == 0:
                totalGPA = False
            else:
                totalGPA = round(sumGPA / sumCredit, 2)

            if totalGPA!= False:
                gpa = totalGPA
            else:
                gpa = "this student has no transcript"
            
            
            return render_template('advisor_transcript.html', transcript = transcript, name = studentName, students = students, gpa = gpa)

        return render_template('advisor_transcript.html', students = students)
    return redirect('/')

#instructor routes----------------------------------------------------------------------------------------------------------------------------------------------------



#admin routes---------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if 'user_id' in session and session['role'] == 'admin':
        return render_template("admin.html")
    return redirect("/")

@app.route('/all_users', methods = ['GET', 'POST'])
def all_users():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if request.method == 'POST':
        role = request.form["role"]
        cursor = mydb.cursor(dictionary = True)
        if role == "applicant":
            cursor.execute("SELECT * FROM user INNER JOIN applicant ON applicant.applicantID = user.uid")
            users = cursor.fetchall()
            user_role = "Applicants"
        elif role == "student":
            cursor.execute("SELECT * FROM user INNER JOIN student ON student.studentid = user.uid")
            users = cursor.fetchall()
            user_role = "Students"
        elif role == "alumni":
            cursor.execute("SELECT * FROM user INNER JOIN alumni ON alumni.alumnid = user.uid")
            users = cursor.fetchall()
            user_role = "Alumni"
        elif role == "instructor":
            cursor.execute("SELECT * FROM user INNER JOIN faculty ON faculty.facultyID = user.uid WHERE faculty.facultyRole = %s", (role,))
            users = cursor.fetchall()
            user_role = "Instructors"
        elif role == "reviewer":
            cursor.execute("SELECT * FROM user INNER JOIN faculty ON faculty.facultyID = user.uid WHERE faculty.facultyRole = %s", (role,))
            users = cursor.fetchall()
            user_role = "Reviewers"
        elif role == "gsec":
            cursor.execute("SELECT * FROM user INNER JOIN faculty ON faculty.facultyID = user.uid WHERE faculty.facultyRole = %s", (role,))
            users = cursor.fetchall()
            user_role = "Graduate Secretaries"
        elif role == "chair":
            cursor.execute("SELECT * FROM user INNER JOIN faculty ON faculty.facultyID = user.uid WHERE faculty.facultyRole = %s", (role,))
            users = cursor.fetchall()
            user_role = "Chairs"
        return render_template("all_users.html", users = users, role = user_role)
    return redirect("/admin")



@app.route('/adminAdvPortal')
def adminAdvPortal():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if session['role'] != 'admin':
        return redirect(url_for('logout'))

    if 'user_id' in session:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT fname FROM user WHERE uid = %s", (session['user_id'],))
        user = cursor.fetchone()
        if user is not None:
            sFname = user['fname']
            return render_template('adminAdvPortal.html', sfname=sFname)
    return redirect(url_for('login'))


@app.route('/register4admin', methods = ['GET', 'POST'])
def register4admin(): 
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if session['role'] != "admin":
        return redirect(url_for('logout'))
    
    message = " "
    error = False 
    
    cursor = mydb.cursor(dictionary=True)

    if request.method == 'POST':
        nextId = request.form["field_uid"]
        username = request.form["field_uname"]
        password = request.form["field_pword"]
        fname = request.form["field_fname"]
        lname = request.form["field_lname"]
        address = request.form["field_address"]
        email = request.form["field_email"]
        role = request.form["field_role"]
        ssn = request.form["field_ssn"]

        if username.strip() == "" or password.strip() == "" or fname.strip() == "" or lname.strip() == "":
            message = "You left a required field blank"
            return render_template("register4admin.html", message = message)

        if role != None:
            cursor.execute("SELECT * FROM user WHERE uid = (%s)", (nextId,))
            idExists = cursor.fetchone()

            if idExists: 
                error = True
                message = "ID is taken"
        
            cursor.execute("SELECT * FROM user WHERE username = (%s)", (username,))
            usernameExists = cursor.fetchone()

            if usernameExists: 
                error = True
                message = "Username is taken"
            
            cursor.execute("SELECT * FROM user WHERE ssn = (%s)", (ssn,))
            passwordExists = cursor.fetchone()

            if passwordExists:
                error = True
                message = "Password is taken"

            if error:
                return render_template('register4admin.html', message = message)
            else:
                if role == "Grad Student Masters":
                    cursor.execute("INSERT INTO user (uid, username, password, fname, lname, address, email, ssn) VALUES ((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))", (nextId, username, password, fname, lname, address, email, ssn,))
                    mydb.commit()
                    cursor.execute("INSERT INTO student (studentid, program, advisorid, rdygrad) VALUES ((%s),(%s),(%s),(%s))", (nextId, "masters", 'NULL', 0, ))
                    message = "Successfully made Account"
                    mydb.commit()
              

                if role == "Grad Student Phd":
                    cursor.execute("INSERT INTO user (uid, username, password, fname, lname, address, email, ssn) VALUES ((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))", (nextId, username, password, fname, lname, address, email, ssn,))
                    mydb.commit()
                    cursor.execute("INSERT INTO student (studentid, program, advisorid, rdygrad) VALUES ((%s),(%s),(%s),(%s))", (nextId, "phd", 'NULL', 0, ))
                    message = "Successfully made Account"
                    mydb.commit()

                if role == "applicant":
                    cursor.execute("INSERT INTO user (uid, username, password, fname, lname, address, email, ssn) VALUES ((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))", (nextId, username, password, fname, lname, address, email, ssn,))
                    mydb.commit()
                    cursor.execute("INSERT INTO applicant (applicantID, applicantStatus) VALUES ((%s),(%s))", (nextId, "Application Materials Missing", ))
                    message = "Successfully made Account"
                    mydb.commit()
                  
                if role == "Grad Secretary":
                    cursor.execute("INSERT INTO user(uid, username, password, fname, lname, address, email) VALUES ((%s),(%s),(%s),(%s),(%s),(%s),(%s))", (nextId, username, password, fname, lname, address, email))
                    mydb.commit()
                    cursor.execute("INSERT INTO faculty(facultyid, facultyRole) VALUES ((%s),(%s))", (nextId, 'gsec'))
                    message = "Successfully made Account"
                    mydb.commit()
 
                if role == "instructor":
                    cursor.execute("INSERT INTO user(uid, username, password, fname, lname, address, email) VALUES ((%s),(%s),(%s),(%s),(%s),(%s),(%s))", (nextId, username, password, fname, lname, address, email))
                    mydb.commit()
                    cursor.execute("INSERT INTO faculty(facultyid, facultyRole) VALUES ((%s),(%s))", (nextId, 'instructor'))
                    message = "Successfully made Account"
                    mydb.commit()

                if role == "chair":
                    cursor.execute("INSERT INTO user(uid, username, password, fname, lname, address, email) VALUES ((%s),(%s),(%s),(%s),(%s),(%s),(%s))", (nextId, username, password, fname, lname, address, email))
                    mydb.commit()
                    cursor.execute("INSERT INTO faculty(facultyid, facultyRole) VALUES ((%s),(%s))", (nextId, 'chair'))
                    message = "Successfully made Account"
                    mydb.commit()
                
                if role == "faculty reviewer":
                    cursor.execute("INSERT INTO user(uid, username, password, fname, lname, address, email) VALUES ((%s),(%s),(%s),(%s),(%s),(%s),(%s))", (nextId, username, password, fname, lname, address, email))
                    mydb.commit()
                    cursor.execute("INSERT INTO faculty(facultyid, facultyRole) VALUES ((%s),(%s))", (nextId, 'faculty reviewer'))
                    message = "Successfully made Account"
                    mydb.commit()

                if role == "admin":
                    cursor.execute("INSERT INTO user(uid, username, password, fname, lname, address, email) VALUES ((%s),(%s),(%s),(%s),(%s),(%s),(%s))", (nextId, username, password, fname, lname, address, email))
                    mydb.commit()
                    cursor.execute("INSERT INTO faculty(facultyid, facultyRole) VALUES ((%s),(%s))", (nextId, 'admin'))
                    message = "Successfully made Account"
                    mydb.commit()
                  
            return render_template('register4admin.html', message = message) 
                
    return render_template('register4admin.html', message = message)
#adminview form of all
#admin view trans of all
#admin can assign adv to student
#admin can view all users
#admin can edit user info
#admin can create new users

#transcript finetuning
#same user multiple thesis issue *COMPLETED*
#and then we done


#register4admin need to be made
#admin routes---------------------------------------------------------------------------------------------------------------------------------------------------------



#applicant routes-----------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/applicantHome', methods=['GET', 'POST'])
def applicantHome():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )

    if session['role'] != "applicant":
        return redirect(url_for('logout'))

    cursor = mydb.cursor(dictionary = True)
    cursor.execute("SELECT applicantID FROM applicant WHERE applicantID = %s", (session["user_id"],))
    studentID = cursor.fetchone()

    return render_template("applicantHome.html", studentID = studentID)

@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor = mydb.cursor(dictionary = True)
    error = False
    
    if request.method == 'POST':
    # fields for applicant
        nextId = request.form["field_uid"]
        username = request.form["field_uname"]
        password = request.form["field_pword"]
        fname = request.form["field_fname"]
        lname = request.form["field_lname"]
        address = request.form["field_address"]
        email = request.form["field_email"]
        role = "applicant"
        ssn = request.form["field_ssn"]

        if username.strip() == "" or password.strip() == "" or fname.strip() == "" or lname.strip() == "":
            message = "You left a required field blank"
            return render_template("register4admin.html", message = message)

        if role == "applicant":
            cursor.execute("SELECT * FROM user WHERE uid = (%s)", (nextId,))
            idExists = cursor.fetchone()

            if idExists: 
                error = True
                message = "ID is taken"
        
            cursor.execute("SELECT * FROM user WHERE username = (%s)", (username,))
            usernameExists = cursor.fetchone()

            if usernameExists: 
                error = True
                message = "Username is taken"
            
            cursor.execute("SELECT * FROM user WHERE ssn = (%s)", (ssn,))
            passwordExists = cursor.fetchone()

            if passwordExists:
                error = True
                message = "Password is taken"

            if error:
                return render_template('createAccount.html', message = message)
            else:
                if role == "applicant":
                    cursor.execute("INSERT INTO user (uid, username, password, fname, lname, address, email, ssn) VALUES ((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))", (nextId, username, password, fname, lname, address, email, ssn,))
                    mydb.commit()
                    cursor.execute("INSERT INTO applicant (applicantID, applicantStatus) VALUES ((%s),(%s))", (nextId, "Application Materials Missing", ))
                    message = "Successfully made Account"
                    mydb.commit()
                    return render_template('createAccount.html', message = message)
    
    return render_template('createAccount.html')


@app.route('/seeStatus', methods=['GET', 'POST'])
def seeStatus():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if session['role'] != "applicant":
        return redirect(url_for('logout'))

    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT username FROM user WHERE uid = %s", (session["user_id"],))
    username = cursor.fetchone()
    cursor.execute ("SELECT applicantStatus FROM applicant WHERE applicantID = %s", (session["user_id"],))
    status = cursor.fetchone()
    return render_template ("seeStatus.html", username = username, status = status)

@app.route("/applicationFillout", methods=['GET', 'POST'])
def applicationFillout():
    return render_template("applicationFillout.html")

@app.route ("/postSubmittingApp", methods=['GET', 'POST'])
def postSubmittingApp():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )

    if request.method == 'POST':
        
        studentID = int (request.form["studentID"])
        
        degreeSeeking = request.form["degreeSeeking"]
        MScheck = request.form["MScheck"]
        MSmajor = request.form["MSmajor"]
        MSuniversity = request.form["MSuniversity"]
        if(request.form["MSgpa"] == ""):
            MSgpa = 0
        else:
            MSgpa = float(request.form["MSgpa"])

        if(request.form["MSyear"] == ""):
            MSyear = 0
        else:
            MSyear = int(request.form["MSyear"])
        BAcheck = request.form["BAcheck"]
        BAmajor = request.form["BAmajor"]
        if(request.form["BAyear"] == ""):
            BAyear = 0
        else:
            BAyear = int(request.form["BAyear"])
        BAuniversity = request.form["BAuniversity"]
        if(request.form["BAgpa"] == ""):
            BAgpa = 0
        else:
            BAgpa = float(request.form["BAgpa"])
        if(request.form["GREverbal"] == ""):
            GREverbal = 0
        else:
            GREverbal = int(request.form["GREverbal"])
        if(request.form["GREquantitative"] == ""):
            GREquantitative = 0
        else:
            GREquantitative = int(request.form["GREquantitative"])
        if(request.form["GREyear"] == ""):
            GREyear = 0
        else:
            GREyear = int(request.form["GREyear"])
        if(request.form["GREadvancedScore"] == ""):
            GREadvancedScore = 0
        else:
            GREadvancedScore = int(request.form["GREadvancedScore"])
        GREadvancedSubject = request.form["GREadvancedSubject"]
        if(request.form["TOEFLscore"] == ""):
            TOEFLscore = 0
        else:
            TOEFLscore = int(request.form["TOEFLscore"])
        TOEFLdata = request.form["TOEFLdata"]
        priorWork = request.form["priorWork"]
        startDate = request.form["startDate"]
        transcriptStatus = "Not Received"
        r1status = "Not Recieved"
        r1writer = request.form["r1writer"]
        r1email = request.form["r1email"]
        r1title = request.form["r1title"]
        r1affiliation = request.form["r1affiliation"]
        r1letter = "Fill When Recieved"
        r2status = "Not Recieved"
        r2writer = request.form["r2writer"]
        r2email = request.form["r2email"]
        r2title = request.form["r2title"]
        r2affiliation = request.form["r2affiliation"]
        r2letter =  "Fill When Recieved"
        r3status = "Not Recieved"
        r3writer =  request.form["r3writer"]
        r3email = request.form["r3email"]
        r3title = request.form["r3title"]
        r3affiliation = request.form["r3affiliation"]
        r3letter =   "Fill When Recieved"
        cursor = mydb.cursor(dictionary= True)

        cursor.execute (
            "INSERT INTO ApplicationForm (studentID, degreeSeeking,MScheck,MSmajor,MSyear,MSuniversity,MSgpa,BAcheck,BAmajor,BAyear,BAuniversity,BAgpa,GREverbal,GREquantitative,GREyear,GREadvancedScore,GREadvancedSubject,TOEFLscore,TOEFLdate,priorWork,startDate,transcriptStatus,r1status,r1writer,r1email,r1title,r1affiliation,r1letter,r2status,r2writer,r2email,r2title,r2affiliation,r2letter,r3status,r3writer,r3email,r3title,r3affiliation,r3letter) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s)", (studentID, degreeSeeking,MScheck,MSmajor,MSyear,MSuniversity,MSgpa,BAcheck,BAmajor,BAyear,BAuniversity,BAgpa,GREverbal,GREquantitative,GREyear,GREadvancedScore,GREadvancedSubject,TOEFLscore,TOEFLdata,priorWork,startDate,transcriptStatus,r1status,r1writer,r1email,r1title,r1affiliation,r1letter,r2status,r2writer,r2email,r2title,r2affiliation,r2letter,r3status,r3writer,r3email,r3title,r3affiliation,r3letter)
        )
        mydb.commit()
        decision = "Application Recieved and Decision Pending"
        cursor.execute("UPDATE applicant SET applicantStatus = %s WHERE applicantID = %s", (decision,session["user_id"],))
        mydb.commit()

        return render_template("applicantHome.html")
    
    return redirect ('/')
#applicant routes----------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/viewApp/<applicantID>', methods=['GET','POST'])
def viewApplication(applicantID):
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )

    cursor = mydb.cursor(dictionary = True)
    cursor.execute("SELECT * FROM ApplicationForm WHERE studentID = %s", (applicantID,))
    form = cursor.fetchone()


    return render_template("viewApp.html", form = form)


@app.route('/FRhome', methods=['GET', 'POST'])
def FRhome():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor = mydb.cursor(dictionary = True)
    cursor.execute("SELECT * FROM applicant")
    applicants = cursor.fetchall()

    return render_template("FRhome.html", applicants = applicants)

@app.route('/email', methods = ['GET', 'POST'])
def email():
    return render_template("email.html")

@app.route('/reviewFormFillout', methods=['GET','POST'])
def reviewFormFillout():
    return render_template("reviewFormFillout.html")


@app.route('/submitReviewForm', methods=['GET','POST'])
def submitReviewForm():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor = mydb.cursor(dictionary = True)
    studentID = request.form["studentID"]
    reviewer = request.form["reviewer"]
    r1rating = request.form["r1rating"]
    r1generic = request.form["r1generic"]
    r1credible = request.form["r1credible"]
    r1from = request.form["r1from"]
    r2rating = request.form["r2rating"]
    r2generic = request.form["r2generic"]
    r2credible = request.form["r2credible"]
    r2from = request.form["r2from"]
    r3rating = request.form["r3rating"]
    r3generic = request.form["r3generic"]
    r3credible = request.form["r3credible"]
    r3from = request.form["r3from"]
    GASrating = request.form["GASrating"]
    deficiencies = request.form["deficiencies"]
    rejectReason = request.form["rejectReason"]
    thoughts = request.form["thoughts"]
    semesterApplied = request.form["semesterApplied"]
    decision = "pending"

    cursor.execute("INSERT INTO ReviewForm (studentID,reviewer,r1rating,r1generic,r1credible,r1from,r2rating,r2generic,r2credible,r2from,r3rating,r3generic,r3credible,r3from,GASrating,deficiencies,rejectReason,thoughts,semesterApplied,decision) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (studentID,reviewer,r1rating,r1generic,r1credible,r1from,r2rating,r2generic,r2credible,r2from,r3rating,r3generic,r3credible,r3from,GASrating,deficiencies,rejectReason,thoughts,semesterApplied,decision,))
    mydb.commit()

    cursor.execute("UPDATE applicant SET applicantStatus = %s WHERE applicantID = %s", ("application reviewed",studentID))
    mydb.commit()
    if session['role'] == "chair":
        return redirect('/chairHome')

    return redirect('/FRhome')

@app.route('/viewReview/<studentID>', methods=['GET','POST'])
def viewReview(studentID):
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )

    if(session['role'] == "chair" or session['role'] == "facultyReviewer"):

        cursor = mydb.cursor(dictionary = True)
        cursor.execute("SELECT * FROM ReviewForm WHERE studentID = %s", (studentID,))
        form = cursor.fetchall()
        return render_template("viewReview.html", form=form)

    else:
        return redirect("/")

@app.route('/chairHome', methods=['GET', 'POST'])
def chairHome():
    mydb = mysql.connector.connect(
        host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
        user="admin",
        password="tommyzackmaya",
        database="university"
    )
    if session['role'] != "chair":
        return redirect("/")

    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT user.username, user.UID, applicant.applicantStatus FROM user INNER JOIN applicant ON user.UID = applicant.applicantID")
    applicants = cursor.fetchall()
    for applicant in applicants:
        if applicant['applicantStatus'] == 'Application Materials Missing':
            applicant['display'] = False
        else:
            applicant['display'] = True

    return render_template("chairHome.html", applicants=applicants)

@app.route('/SAdeleteApp/<username>', methods=['GET', 'POST'])
def SAdeleteApp(username):
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor = mydb.cursor(dictionary = True)
    cursor.execute("DELETE FROM user WHERE username = %s", (username,))
    mydb.commit()
    cursor.execute("SELECT user.username, user.UID, user.password, user.email, applicant.applicantStatus FROM user INNER JOIN applicant ON user.UID = applicant.applicantID")
    people = cursor.fetchall()

    return render_template("SAseeapplicants.html", people=people)
    
@app.route('/SAseeapplicants', methods=['GET', 'POST'])
def SAseeapplicants():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    cursor = mydb.cursor(dictionary = True)

    cursor.execute("SELECT user.username, user.UID, user.password, user.email, applicant.applicantStatus FROM user INNER JOIN applicant ON user.UID = applicant.applicantID")
    people = cursor.fetchall()

    return render_template("SAseeapplicants.html", people=people)

#alumni routes^------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/alumni', methods=['GET', 'POST'])
def alumni():
    mydb = mysql.connector.connect(
    host="phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com",
    user="admin",
    password="tommyzackmaya",
    database="university"
    )
    if session['role'] != "alumni" and session['role'] != "gsec" and session['role'] != "admin" and session['role'] != "instructor":
        return redirect(url_for('logout'))
    
    if 'user_id' in session:
        cursor = mydb.cursor(dictionary=True)
        cursor2 = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE uid = %s", (session['user_id'],))
        user = cursor.fetchone()

        if user is not None:
            # Check if the user is in the alumni table
            cursor.execute("SELECT * FROM alumni WHERE alumnid = %s", (session['user_id'],))
            alumni_user = cursor.fetchone()
            if alumni_user is not None:
                # Fetch alumni data for the signed in user
                if request.method == 'POST':
                    new_email = request.form['email']
                    new_addy = request.form['address']
                    cursor.execute("UPDATE user SET email=(%s), address=(%s) WHERE uid=(%s)", (new_email, new_addy, session['user_id'],))
                    mydb.commit()

                cursor.execute("SELECT * FROM alumni JOIN user ON alumni.alumnid = user.uid WHERE alumni.alumnid = %s", (session['user_id'],))
                alumni_data = cursor.fetchone()
                
                # Fetch alumni transcript data based on uid or username
                cursor.execute("SELECT * FROM transcript JOIN course ON transcript.cid = course.cid WHERE transcript.tuid = %s", (session['user_id'],))
                transcript_data = cursor.fetchall()

                #Get all courses
                cursor2.execute("SELECT * FROM transcript JOIN course ON transcript.cid = course.cid WHERE transcript.tuid=(%s)", (session['user_id'],))
                courses = cursor2.fetchall()

                #calculate GPA in accordance to GWU GPA policy, = sumGPA / Credit Hours
                #A, 4.0; A−, 3.7; B+, 3.3; B, 3.0; B−, 2.7; C+, 2.3; C, 2.0; C−, 1.7; and F, 0
                GPA = {
                    'A':4.0,
                    'A-':3.7,
                    'B+':3.3,
                    'B':3.0,
                    'B-':2.7,
                    'C+':2.3,
                    'C':2.0,
                    'F':0
                        }
                #sum of GPA
                sumGPA = 0
                #Total of credit hours
                sumCredit = 0
                #cumalative GPA
                totalGPA = 0

                #ctr
                ctr = 0
                belowBcounter = 0
                for course in courses:
                    if course['grade'] != 'IP':
                        sumGPA+= GPA[course['grade']] * course['credits']
                        ctr+=1
                        sumCredit+= course['credits']
                
                if ctr == 0:
                    totalGPA = False
                else:
                    totalGPA = round(sumGPA / sumCredit, 2)

                if totalGPA!= False:
                    gpa = totalGPA
                else:
                    gpa = "this student has no transcript"

                return render_template('alumni.html', alumni_data=alumni_data, transcript_data=transcript_data, username=user['username'], is_faculty=False, gpa = gpa)

            # Check if the user is in the faculty table
            cursor.execute("SELECT * FROM faculty WHERE facultyid = %s", (session['user_id'],))
            faculty_user = cursor.fetchone()
            if faculty_user is not None:
                # Fetch all alumni data for faculty members
                cursor.execute("SELECT * FROM alumni JOIN user ON alumni.alumnid = user.uid;")
                alumni_data = cursor.fetchall()

                return render_template('alumni.html', alumni_data=alumni_data, username=user['username'], is_faculty=True)

    # User is not signed in as either an alumni or faculty member
    return redirect(url_for('login'))

#alumni routes^-----------------------------------------------------------------------------------------------------------------------------------------------------



app.run(host='0.0.0.0', port=5000)