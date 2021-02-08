import dotenv
import os
from canvasapi import Canvas
import sys

if len(sys.argv) != 2:
    print('Usage: {} <course_id>'.format(sys.argv[0]))
    sys.exit(1)

course_id = sys.argv[1]

dotenv.load_dotenv()

canvas_url = 'https://moravian.instructure.com/'
canvas_token = os.environ['CANVAS_TOKEN']
canvas = Canvas(canvas_url, canvas_token)

course = canvas.get_course(course_id)
print('Course name: {}'.format(course.name))

for assignment_group in course.get_assignment_groups():
    print('{}:{} - {}'.format(course_id, assignment_group.id, assignment_group.name))




