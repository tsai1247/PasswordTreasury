# python 3.7 up
from datetime import datetime
import sqlite3
from sql_commands import sql_commands
from AES import AES
import json

class Data():
    def __init__(self, path='data.db') -> None:
        self.path = path
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()

        try:
            self.init()
        except:
            pass

    def execute(self, command: str, condition = None, parameters = None):
        if condition is not None:
            command = command.replace('[CONDITION]', condition)
        if parameters is None:
            parameters = ()
        return self.cur.execute(command, parameters)

    def commit(self):
        return self.con.commit()

    def init(self):
        self.execute(sql_commands.TREASURY_CREATE)
        self.commit()

    def load(self, platform = None, account= None):
        # input: 無(未來會是query)
        # 成功output: list[tuple(平台, 帳號, 密碼, 備註, 更新時間, 創建時間)]
        # 失敗output: 讀寫失敗
        condition = ''
        parameters = []
        if platform:
            condition += f' AND Platform = ?'
            parameters.append(platform)
        if account:
            condition += f' AND Account = ?'
            parameters.append(account)

        return self.execute(sql_commands.TREASURY_SEARCH, condition, parameters).fetchall()

    def add(self, platform, account, password, remark, modifyDate = datetime.now(), createDate = datetime.now()):
        # input: tuple(平台, 帳號, 密碼, 備註)
        # 成功output: 成功
        # 失敗output: 讀寫失敗、平台-帳號 重複
        self.execute(sql_commands.TREASURY_INSERT, None, (platform, account, password, remark, modifyDate, createDate))
        return self.commit()

    def delete(self, platform=None, account=None):
        # input: tuple(平台-帳號)
        # 成功output: 成功、未刪除任何資料
        # 失敗output: 讀寫失敗
        condition = ''
        parameters = []
        if platform:
            condition += f' AND Platform = ?'
            parameters.append(platform)
        if account:
            condition += f' AND Account = ?'
            parameters.append(account)

        self.execute(sql_commands.TREASURY_DELETE, condition, parameters)
        return self.commit()

    def update():
        pass
        # input: tuple(平台, 帳號, 密碼=None, 備註=None)
        # 成功output: 成功、未更新任何資料
        # 失敗output: 讀寫失敗


class Safty_Data(Data):
    def __init__(self, path, password) -> None:
        self.password = password
        super().__init__(path)
    
    def init(self):
        return super().init()

    def load(self, platform=None, account=None):
        ret = super().load(platform, account)
        for i in range(len(ret)):
            tmp = list(ret[i])
            for j in range(len(tmp)):
                try:
                    json.loads(tmp[j])
                    tmp[j] = AES(self.password).decrypt(tmp[j])
                except:
                    pass
            ret[i] = tuple(tmp)
        return ret

    def add(self, platform, account, password, remark, modifyDate=datetime.now(), createDate=datetime.now()):
        password = AES(self.password).encrypt(str(password)).get()
        return super().add(platform, account, password, remark, modifyDate, createDate)
    
    def delete(self, platform=None, account=None):
        return super().delete(platform, account)
    
    def update():
        pass

