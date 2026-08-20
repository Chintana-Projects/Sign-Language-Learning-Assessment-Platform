from app.analytics.attempt_tracker import AttemptTracker


student_trackers = {}


def get_tracker(student_id):

    if student_id not in student_trackers:

        student_trackers[student_id] = AttemptTracker(
            student_id
        )

    return student_trackers[student_id]