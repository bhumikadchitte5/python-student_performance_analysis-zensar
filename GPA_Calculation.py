import mysql.connector
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
DB_CONFIG={
    "host":"localhost",
    "user":"root",
    "password":"bdc@2615",
    "database":"python_project"
}
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
def calculate_gpa(grades, credits):
    grade_points = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
    total_points = 0
    total_credits = 0

    for i in range(len(grades)):
        grade_point = grade_points.get(grades[i])  
        total_points += grade_point * credits[i]
        total_credits += credits[i]

    if total_credits > 0:
        result = total_points / total_credits
        return round(result, 2)
    else:
        return 0.0  


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            conn=get_connection()
            cursor=conn.cursor(dictionary=True)
            if self.path.startswith("/student/"):
                student_id=self.path.split("/")[-1]
                #query for grade from grades table
                cursor.execute("select grade from grades where student_id=%s",(student_id,))
                grades_data = cursor.fetchall()
                grade=[i['grade'] for i in grades_data]
                # print(grades_data)
                # print(grade)
                #query for credits from course table
                cursor.execute("""
                    SELECT credit 
                    FROM courses 
                    WHERE course_id IN (
                    SELECT course_id 
                    FROM grades 
                    WHERE student_id = %s
                )""", (student_id,))
                credits_data = cursor.fetchall()
                credits=[i['credit'] for i in credits_data]
                # print(credits)
                # print(credits_data)
                gpa=calculate_gpa(grade,credits)
                print(f"Student_ID:{student_id}  GPA:{gpa}")
                response = {"student_id": student_id, "GPA": gpa}
                response_body = json.dumps(response)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(response_body.encode())
        except Exception as e:
            self.send_error(500, str(e))
        finally:
            cursor.close()
            conn.close()

def run(server_class=HTTPServer, handler_class=RequestHandler,port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__=="__main__":
    run()