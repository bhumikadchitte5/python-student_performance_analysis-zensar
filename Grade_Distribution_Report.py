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
def grade_distribution(grades):
    grade_count={'A':0,'B':0,'C':0,'D':0,'F':0}
    for g in grades:
        if g in grade_count:
            grade_count[g]+=1
    return grade_count

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            if self.path.startswith("/student/"):
                query = "SELECT grade FROM grades"
                cursor.execute(query)
                result = cursor.fetchall()
                # print(result)
                grades=[i['grade']for i in result]
                print(grades)
                print(f"Grade Distribution Report:\n{grade_distribution(grades)}")
                res=grade_distribution(grades)
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode())  
        except Exception as e:
            self.send_error(500, str(e))
        finally:
            cursor.close()

def run(server_class=HTTPServer, handler_class=RequestHandler,port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__=="__main__":
    run()
