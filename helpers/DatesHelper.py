from datetime import timedelta
import random


class DatesHelper:
    @staticmethod
    def random_between(start, end):
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return start + timedelta(seconds=random_second)
