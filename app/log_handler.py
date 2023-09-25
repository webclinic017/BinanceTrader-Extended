
class LogHandler:

    def __init__(self) -> None:
        self.logs_bclient = []
    

    def add_bclient_log(self, msg):
        self.logs_bclient.append(msg)


    def get_bclient_logs(self) -> list:
        return self.logs_bclient
    



myLogHandler = LogHandler()
