from datetime import datetime


class NotificationService:

    def __init__(self):
        self.notifications = {}

    def add_notification(
        self,
        student_id: str,
        title: str,
        message: str,
        notification_type: str
    ):

        student_id = str(student_id)

        if student_id not in self.notifications:
            self.notifications[student_id] = []

        self.notifications[student_id].insert(
            0,
            {
                "title": title,
                "message": message,
                "type": notification_type,
                "created_at": datetime.now().isoformat(),
                "read": False
            }
        )

    def get_notifications(
        self,
        student_id: str
    ):

        return self.notifications.get(
            str(student_id),
            []
        )

    def mark_all_read(
        self,
        student_id: str
    ):

        for notification in self.notifications.get(
            str(student_id),
            []
        ):
            notification["read"] = True

        return True