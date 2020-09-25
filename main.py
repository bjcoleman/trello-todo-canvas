
import os
import datetime
import logging
from collections import namedtuple
import time

import dotenv
from canvasapi import Canvas
from trello import TrelloClient
from history_db import RedisHistoryDB

Assignment = namedtuple(typename='Assignment', field_names=['name', 'assignment_id', 'assignment_group', 'course_name', 'course_id', 'due_at', 'html_url'])

logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s: %(message)s",
                          datefmt="%Y-%m-%d - %H:%M:%S")
fh = logging.FileHandler("trello-todo-canvas.log", "w")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)


def get_watched_courses():
    h = RedisHistoryDB()
    return h.get_courses()


def get_past_assignments(course_ids):
    canvas_url = 'https://moravian.instructure.com/'
    canvas_token = os.environ['CANVAS_TOKEN']

    logger.info('Connecting to Canvas')
    canvas = Canvas(canvas_url, canvas_token)

    ret = []

    for course_id in course_ids:
        logger.info('Reading course data for course id {}'.format(course_id))
        course = canvas.get_course(course_id)
        course_name = course.name

        logger.info('Reading assignments for course id {}'.format(course_id))
        for assignment in course.get_assignments(bucket='past'):
            ret.append(Assignment(assignment.name, assignment.id, assignment.assignment_group_id,
                              course_name, assignment.course_id,
                              assignment.due_at, assignment.html_url))

    return ret


def in_db(assignment):
    h = RedisHistoryDB()
    return h.is_registered(assignment)


def in_skipped_group(assignment):
    h = RedisHistoryDB()
    return h.is_skipped(assignment.course_id, assignment.assignment_group)


def update_trello(assignments):
    trello_api_key = os.environ['TRELLO_API_KEY']
    trello_secret = os.environ['TRELLO_TOKEN']

    logger.info('Connecting to Trello')
    client = TrelloClient(
        api_key=trello_api_key,
        api_secret=trello_secret
    )

    logger.info('Reading Trello boards')
    for board_obj in client.list_boards():
        if board_obj.name == 'Work TODO':
            todo_board = board_obj

    logger.info('Reading Trello lists')
    for list_obj in todo_board.list_lists():
        if list_obj.name == 'Teaching':
            teaching_list = list_obj

    for assignment in assignments:
        if not in_db(assignment):
            if not in_skipped_group(assignment):
                teaching_list.add_card('Grade ' + assignment.course_name + ': ' + assignment.name, 'Grade',
                                   due=str(datetime.datetime.now() + datetime.timedelta(days=7)))
                add_to_db(assignment)
                logger.info(
                    'Added Assignment {}:{}'
                    .format(assignment.course_id, assignment.assignment_id))
            else:
                logger.info('Skipped Assignment {}:{} (In Skip Group)'
                            .format(assignment.course_id, assignment.assignment_id))
        else:
            logger.info('Skipped Assignment {}:{} (In DB)'
                        .format(assignment.course_id, assignment.assignment_id))


def add_to_db(assignment):
    h = RedisHistoryDB()
    logger.info('Registering assignment {}:{} in DB'.format(assignment.course_id, assignment.assignment_id))
    h.register_assignment(assignment)


def go():
    while True:
        update_trello(get_past_assignments(get_watched_courses()))
        time.sleep(3600)


if __name__ == '__main__':
    # Sleep for a minute to make sure the OS/network are ready
    time.sleep(60)
    dotenv.load_dotenv()
    go()
