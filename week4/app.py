from flask import Flask, render_template, request
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        try:

            tmarks = 0
            mx = 0
            count = 0
            flag = False
            mrks = []
            tp = request.form["ID"]
            csid = int(request.form['id_value'])

            with open('data.csv', 'r') as file:
                file.readline()
                data = file.readlines()
                file.close()

            if tp == 'student_id':
                Webpage = 'Student Data'
                title = 'Student Details'
                for line in data:
                    line = line.split(",")
                    if int(line[0]) == int(csid):
                        tmarks += int(line[2])
                        flag = True
                return render_template('temp.html', tp=tp, flag=flag, title=title, Webpage=Webpage, csid=csid,data=data, tmarks=tmarks)

            elif tp == 'course_id':
                Webpage = 'Course Data'
                title = 'Course Details'
                for line in data:
                    line = line.split(',')
                    if int(line[1]) == int(csid):
                        flag = True
                        tmarks += int(line[2])
                        count += 1
                        mrks.append(int(line[2]))
                        if int(line[2]) > mx:
                            mx = int(line[2])
                if count > 0:
                    avr = tmarks / count
                else:
                    avr = 0

                plt.hist(mrks, bins=10)
                plt.xlabel('Marks')
                plt.ylabel('Frequency')
                plt.savefig('static/plot.png')
                return render_template('temp.html', tp=tp, flag=flag, title=title, Webpage=Webpage, csid=csid,
                                       data=data, tmarks=tmarks, avr=avr, mx=mx)

            else:
                Webpage = 'Something Went Wrong'
                title = 'Wrong Inputs'

                return render_template('temp.html',  title=title, Webpage=Webpage)

        except Exception :
            Webpage = 'Something Went Wrong'
            title = 'Wrong Inputs'
            flag=False
            return render_template('temp.html',flag=flag, title=title, Webpage=Webpage)

if __name__ == '__main__':
    app.run()