class AchievementEngine:

    def generate(self, profile):

        achievements = []

        completed = len(profile.get("completed_letters", []))
        sessions = profile.get("total_sessions", 0)
        attempts = profile.get("total_attempts", 0)

        mastery = profile.get("alphabet_mastery", {})

        mastered = sum(
            1
            for data in mastery.values()
            if data.get("accuracy", 0) >= 90
        )

        if attempts >= 1:
            achievements.append({
                "title": "First Practice",
                "icon": "🎯"
            })

        if completed >= 1:
            achievements.append({
                "title": "First Letter",
                "icon": "📝"
            })

        if completed >= 5:
            achievements.append({
                "title": "Alphabet Explorer",
                "icon": "🔤"
            })

        if mastered >= 5:
            achievements.append({
                "title": "Master Learner",
                "icon": "🏆"
            })

        if sessions >= 10:
            achievements.append({
                "title": "Dedicated Learner",
                "icon": "🔥"
            })

        return achievements