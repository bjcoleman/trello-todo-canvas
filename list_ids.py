
"""
This program lists all the active courses as well
as courses with an assignment group containing "Ungraded"

This is useful for configuring the Redis db (See README.md)
"""

import os

import dotenv
from canvasapi import Canvas

dotenv.load_dotenv()

canvas_url = 'https://moravian.instructure.com/'
canvas_token = os.environ['CANVAS_TOKEN']

canvas = Canvas(canvas_url, canvas_token)

print('Current Courses:')
for course in canvas.get_courses():
    print('{}: {}'.format(course.id, course.name))

print('\n\nUngraded Assignment Groups:')
# 2020 course ids
course_ids = [14245, 14692, 13514, 13520]

for course_id in course_ids:
    course = canvas.get_course(course_id)
    for group in course.get_assignment_groups():
        if 'Ungraded' in group.name:
            print('{}:{}'.format(course_id, group.id))
