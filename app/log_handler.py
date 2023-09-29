from datetime import datetime

class LogHandler:

    def __init__(self) -> None:
        self.logs_error = []
        self.logs_bclient = []
        self.logs_btrader_info = {}
        self.logs_btrader_special = {}
        self.logs_btrader_all_special = []
    

    ################ functional
    def cook_msg(self, msg: str, level: str, trader_id = -2) -> str:
        current_time = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        text1 = f"{current_time} ({level}) bTrader: {str(trader_id)}: {str(msg)}"
        return text1


    ################ self/error
    def add_error_log(self, msg: str, level: str, trader_id: int) -> None:
        text1 = self.cook_msg(msg=msg, level=level, trader_id=trader_id)
        self.logs_error.append(text1)
        print(text1)


    def get_error_logs(self) -> list:
        return self.logs_error
    

    ################ bclient
    def add_bclient_log(self, msg, level="info") -> None:
        text1 = self.cook_msg(msg=msg, level="critical", trader_id=-3)
        self.logs_bclient.append(text1)


    def get_bclient_logs(self) -> list:
        return self.logs_bclient
    
    
    ################ btrader
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

            if level == "error" or level == "critical":
                self.add_error_log(msg=msg, level=level, trader_id=btrader_id)
        except Exception as e:
            self.add_error_log(msg=str(e), level="critical", trader_id=-2)


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
