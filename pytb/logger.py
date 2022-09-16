import time


class Logger:
    """Handles creating and reading logs
    """

    def __init__(self):
        """Logger init
        """
        self.start_time = time.time()
        self.wins = 0
        self.losses = 0
        self.fights = 0
        self.unfollows = 0
        self.follows = 0
        self.restarts = 0
        self.accounts_examined = 0
        self.blocks = 0

    def make_timestamp(self):
        """creates a time stamp for log output

        Returns:
            str: log time stamp
        """
        output_time = time.time() - self.start_time
        output_time = int(output_time)

        time_str = str(self.convert_int_to_time(output_time))

        output_string = time_str

        return output_string

    def convert_int_to_time(self, seconds):
        """convert epoch to time

        Args:
            seconds (int): epoch time in int

        Returns:
            str: human readable time
        """
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d:%02d:%02d" % (hour, minutes, seconds)

    def log(self, message):
        """add message to log

        Args:
            message (str): message to add
        """
        print(f"{self.make_timestamp()}||{self.unfollows} unfollows ||{self.follows} follows||{self.accounts_examined} accounts examined|| {self.blocks} accounts blocked||{self.restarts} restarts: {message}")

    def add_win(self):
        """add win to log
        """
        self.wins += 1

    def add_loss(self):
        """add loss to log
        """
        self.losses += 1

    def add_fight(self):
        """add fight to log
        """
        self.fights += 1

    def add_unfollow(self):
        """add unfollow tally to log
        """
        self.unfollows += 1

    def add_follow(self):
        """add unfollow tally to log
        """
        self.follows += 1

    def remove_follow(self):
        """add unfollow tally to log
        """
        self.follows -= 1

    def add_restart(self):
        """add restart to log
        """
        self.restarts += 1

    def add_account_examined(self):
        """add restart to log
        """
        self.accounts_examined += 1

    def add_block(self):
        """add restart to log
        """
        self.blocks += 1

