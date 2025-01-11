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
            if student_id:
                query = f"""
                SELECT s.student_id, s.first_name,s.last_name,
                    (SELECT GROUP_CONCAT(c.course_name) 
                        FROM courses c 
                        WHERE c.course_id IN 
                        (SELECT g.course_id FROM grades g WHERE g.student_id = s.student_id)) AS courses,
                        (SELECT GROUP_CONCAT(g.grade) 
                        FROM grades g 
                        WHERE g.student_id = s.student_id) AS grades
                FROM student s
                WHERE s.student_id = %s
                """
                cursor.execute(query, (student_id,))
            result = cursor.fetchall()
            cursor.close()
            response_body = json.dumps(result)
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