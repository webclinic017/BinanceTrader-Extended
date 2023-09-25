
class LogHandler:

    def __init__(self) -> None:
        self.logs_bclient = []
        self.logs_btrader_info = {"a": []}
        self.logs_btrader_special = {"a": []}
        self.logs_btrader_all_special = []
    

    def add_bclient_log(self, msg) -> None:
        self.logs_bclient.append(msg)


    def get_bclient_logs(self) -> list:
        return self.logs_bclient
    

    def add_btrader_log(self, btrader_id: int, level: str, msg: str) -> None:
        try:
            log = {
                "btrader_id": btrader_id,
                "level": level,
                "msg": msg
            }
            if str(btrader_id) not in self.logs_btrader_info:
                self.logs_btrader_info[str(btrader_id)] = []
            if str(btrader_id) not in self.logs_btrader_special:
                self.logs_btrader_special[str(btrader_id)] = []

            self.logs_btrader_info[str(btrader_id)].append(log)
            self.logs_btrader_info[str(btrader_id)] = self.logs_btrader_info[str(btrader_id)][-200:]

            if level != "info":
                self.logs_btrader_all_special.append(log)
                self.logs_btrader_all_special = self.logs_btrader_all_special[-300:]

            if level != "info":
                self.logs_btrader_special[str(btrader_id)].append(log)
        except Exception as e:
            print(e)


    def get_btrader_logs_all_special(self) -> list:
        print(f"logs_btrader_all_special: {self.logs_btrader_all_special}")
        print(f"logs_btrader_all_special: {self.logs_btrader_info}")
        print(f"logs_btrader_all_special: {self.logs_btrader_special}")
        return self.logs_btrader_all_special
    

    def get_btrader_logs_special(self, btrader_id: int, level = "all") -> list:
        if level == "all":
            return self.logs_btrader_special[str(btrader_id)]
        
        __btrader_logs_level = []
        for log in self.logs_btrader_special[str(btrader_id)]:
            if log["level"] == level:
                __btrader_logs_level.append(log)

        return __btrader_logs_level


    def get_btrader_logs_info(self, btrader_id: int) -> list:
        return self.logs_btrader_info[str(btrader_id)]


myLogHandler = LogHandler()
