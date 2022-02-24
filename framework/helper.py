import time

class timehelper():

    @staticmethod
    def get_remaining_time(t):
        """
        Returns the remaining time in seconds from a given time.
        """
        return time.time() - t 

    @staticmethod
    def convert_seconds_2_words(remaining, granularity=None):

        if granularity is None:
            granularity = 1

        intervals = (
            ('weeks', 604800),  # 60 * 60 * 24 * 7
            ('days', 86400),    # 60 * 60 * 24
            ('hours', 3600),    # 60 * 60
            ('minutes', 60),
            ('seconds', 1),
        )

        result = []

        for name, count in intervals:
            value = remaining // count
            if value:
                remaining -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(int(value), name))

        
        return ', '.join(result[:granularity]) + " ago" if len(result) > 1 else "1 second ago"

    @staticmethod
    def check_if_one_hour_since(t):
        """
        Returns True if the time is one hour since the given time.
        """
        return time.time() - t > 3600