class ScreeningAI:

    def screen_candidate(self, ats_score):

        if ats_score >= 75:
            return "Shortlisted"

        return "Rejected"