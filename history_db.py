
from redis import Redis


class RedisHistoryDB:

    def __init__(self):
        self.connect()

    def connect(self):
        self.db = Redis('localhost', 6379)

    def num_assignments(self):
        return self.db.scard('assignments')

    def register_assignment(self, assignment):
        key = '{}:{}'.format(assignment.course_id, assignment.assignment_id)
        self.db.sadd('assignments', key)

    def is_registered(self, assignment):
        key = '{}:{}'.format(assignment.course_id, assignment.assignment_id)
        return self.db.sismember('assignments', key)

    def get_courses(self):
        # returns a set of ASCII strings
        return [int(x) for x in self.db.smembers('courses')]

    def is_skipped(self, course_id, assignment_group):
        key = '{}:{}'.format(course_id, assignment_group)
        return self.db.sismember('skip', key)
