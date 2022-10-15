from asyncio.windows_events import NULL
import sqlite3


class Database:
    def __init__(self, db_file) :
        self.conection = sqlite3.connect(db_file)
        self.cursor = self.conection.cursor()
    
    def is_exist(self, user_id):
        request_ = "SELECT * FROM `users` WHERE `user_id` = ? OR `user_number` = ?"
        with self.conection:
            res = self.cursor.execute(request_, (user_id,user_id,)).fetchmany(1)
        return bool(res)

    def is_active(self, user_id):
        request_ = "SELECT `active` FROM `users` WHERE `user_id` = ?"
        with self.conection:
            res = self.cursor.execute(request_, (user_id,))
        return bool(int(res[0]))

    def add_user(self, user_number, user_id = NULL):
        try:
            request_ = "INSERT INTO `users` (`user_number`,`user_id`) VALUES (?,?)"
            with self.conection:
                self.cursor.execute(request_,(user_number,user_id,))
                return True
        except:
            request_ = "UPDATE `users` SET `user_id`= ? WHERE user_number = ?"
            with self.conection:
                self.cursor.execute(request_, (user_id, user_number,))
                return False

    def add_numbers(self, user_list):
        user_list.append(0)
        print(user_list)
        count = 0
        for user in user_list:
            if self.add_user(user):
                count += 1
        return count



    def get_count(self):
        # код закоментирован по причине невнятного формата вывода (не цифра), ради которого было наслоено .fetchmany(1)[0][0]
        # в качестве альтернативы заюзан костыль
        return len(self.get_users())
        # request_ = "SELECT COUNT(user_number) FROM users"
        # with self.conection:
        #     print(self.cursor.execute(request_))
        #     return int(self.cursor.execute(request_).fetchmany(1)[0][0])

    def get_users(self, range_start = 0, range_end = -1):
        request_ = "SELECT `user_number`, `user_id`, `active`, `id` FROM `users`"
        with self.conection:
            return list(self.cursor.execute(request_))[range_start:range_end]

    def get_active_users(self, range_start=0, range_end=-1):
        request_ = "SELECT `user_number`, `user_id`, `active`, `id` FROM `users` WHERE active = 1"
        with self.conection:
            return list(self.cursor.execute(request_))[range_start:range_end]

    def set_active(self, user_number, active):
        active = int(bool(active))
        request_ = "UPDATE `users` SET `active`= ? WHERE user_number = ?"
        with self.conection:
            return self.cursor.execute(request_, (active, user_number))






