import mysql.connector
from http.server import HTTPServer,BaseHTTPRequestHandler
import json

DB_CONFIG={
    "host":"localhost",
    "user":"root",
    "password":"bdc@2615",
    "database":"python_project"
}
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def notify_grade_change(student_id, course_id, old_grade, new_grade):
    if old_grade != new_grade:
        message = (f"Notification: Student ID {student_id}, your grade for course {course_id} "
                   f"has been updated from {old_grade} to {new_grade}.")
        return message
    return None

class RequestHandler(BaseHTTPRequestHandler):
    def do_PUT(self):
        try:
            length=int(self.headers["content-length"])
            data=json.loads(self.rfile.read(length))
            conn=get_connection()
            cursor=conn.cursor()
            student_id=data['student_id']
            course_id=data['course_id']
            new_grade=data['new_grade']
            query="select grade from grades where student_id=%s and course_id=%s"
            cursor.execute(query,(student_id,course_id))
            result=cursor.fetchone()
            # print(result)
            if result:
                old_grade=result[0]
                # print(result[0])
                cursor.execute(
                    "UPDATE grades SET grade = %s WHERE student_id = %s AND course_id = %s",
                    (new_grade, student_id, course_id)
                )
                conn.commit()
                print(notify_grade_change(student_id, course_id, old_grade, new_grade))
                notification = notify_grade_change(student_id, course_id, old_grade, new_grade)
                if notification:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(notification.encode())
                else:
                    self.send_response(204)  # No content, since no change occurred
                    self.end_headers()
            else:
                self.send_error(404, "Record not found")

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


