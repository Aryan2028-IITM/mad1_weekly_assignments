from jinja2 import Template

import sys
import matplotlib.pyplot as plt
def main():
    avr=0


    TEMPLATE ="""
    <!DOCTYPE html>
    <html>
    <head>
    <title>{{ Webpage }}</title>
    </head>
    <body><div>
    <h1>{{ title }}</h1></div>
    <div>
    {% if arg1 == "-s" and flag %}
    <table border="1">
    <thead>
    <tr>
    <th>Student ID</th>
    <th>Course ID</th>
    <th>Marks</th>
    </tr>
    </thead>
    <tbody>
    {% for row in data %}
    {% set row= row.split(",") %}
    {% set id=row[0]|int %}
    {% if id == arg2 %}
    <tr>
    <td>{{ arg2 }}</td>
    <td>{{ row[1] }}</td>
    <td>{{ row[2] }}</td>
    </tr>
    {% endif %}
    {% endfor %}
    <tr>
    <td colspan="2"  align = "center">Total Marks</td>
    <td>{{ tmarks }}</td>
    </tr>
    </tbody>
    </table>
    {% elif arg1 == "-c" and flag %}
    <table border = "1">
    <thead>
    <tr>
    <th>Average Marks</th>
    <th>Maximum Marks</th>
    </tr>
    </thead>
    <tbody>
    <tr>
    <td>{{avr}}</td>
    <td>{{mx}}</td>
    </tr>
    </tbody>
    </table>
    </div>
    <div>
    <img src="plot.png" alt="Histogram">
    </div>
    {% else %}
    <p>Something went wrong</p>
    {% endif %}
    </div>
    </body>
    </html>
    """

    # noinspection PyBroadException
    flag=False
    try:
        arg1 = sys.argv[1]
        arg2 = int(sys.argv[2])
        mrks = []
        tmarks = 0
        mx = 0

        count = 0
        file = open('data.csv', "r")
        file.readline()

        data = file.readlines()
        file.close()
        if arg1 == "-s":

            for line in data:
                line = line.split(",")
                if int(line[0]) == arg2:
                    tmarks += int(line[2])
                    flag=True
            if flag:
                webpage = "Student Data"
                title = "Student Details"
            else:
                webpage = "Something Went Wrong"
                title = "Wrong Inputs"
        elif arg1 == "-c":
            webpage = "Course Data"
            title = "Course Details"
            for line in data:
                line = line.split(",")
                if int(line[1]) == arg2:
                    tmarks += int(line[2])
                    count += 1
                    mrks.append(int(line[2]))
                    if int(line[2]) > mx:
                        mx = int(line[2])

            avr = tmarks / count
            tmarks = 0
            flag=True
            plt.hist(mrks, bins=10)
            plt.xlabel('Marks')
            plt.ylabel('Frequency')
            plt.savefig('plot.png')
        else:
            webpage = "Something Went Wrong"
            title = "Wrong Inputs"
        template = Template(TEMPLATE)
        content = template.render(title=title, flag=flag ,Webpage=webpage, arg1=arg1, arg2=arg2, data=data, tmarks=tmarks, avr=avr,mx=mx)
        file = open("output.html", "w")
        file.write(content)
        file.close()
    except:
        webpage="Something Went Wrong"
        title="Wrong Inputs"
        template = Template(TEMPLATE)
        content=template.render(title=title,Webpage=webpage)
        file=open("output.html","w")
        file.write(content)
        file.close()
if __name__ == "__main__":

    main()