from datetime import timedelta
import random


class DatesHelper:
    """
    All methods and variables to help manipulate dates.
    """

    @staticmethod
    def random_between(start, end):
        """
        Generate a random date between the given two.
        :param start: From email boundary (included).
        :param end: To email boundary (excluded).
        :return: Generated random date.
        """
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return start + timedelta(seconds=random_second)
