import sqlite3

class Database():
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()      

        #table
        self.USER_INFO = 'USER_INFO'
        self.STEEM_USER = 'STEEM_USER'
        self.USER_CHANNEL = 'USER_CHANNEL'

        #columns
        self.user_id = "user_id"
        self.username = "username"      
        self.steem_username = "steem_username"
        self.steem_post = "steem_post"
        self.post_date = "post_date"
        self.channel_id = 'channel_id'
    pass
        
    def create_table(self):
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {self.USER_INFO} ({self.user_id} INTEGER PRIMARY KEY, {self.username} TEXT)''')
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {self.STEEM_USER} ({self.steem_username} TEXT PRIMARY KEY, {self.steem_post} TEXT, {self.post_date} TEXT)''')
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {self.USER_CHANNEL} ({self.channel_id} INTEGER, {self.user_id} INT)''')
        self.conn.commit()

    def insert_user_data(self, user_id, username):
        self.c.execute(f"INSERT OR REPLACE INTO {self.USER_INFO} ({self.user_id}, {self.username}) VALUES (?, ?)", (user_id, username))
        self.conn.commit()

    def delate_user(self, user_ids):
        for user_id in user_ids:
            self.c.execute(f"DELETE FROM {self.USER_INFO} WHERE {self.user_id} = ?", (user_id,)) 
        self.conn.commit()          
    
    def get_user_data(self, user_id):
        self.c.execute(f'''SELECT {self.user_id} FROM {self.USER_INFO} WHERE {self.user_id} = ?''', (user_id,))
        result = self.c.fetchone()
        self.conn.commit()
        return result[0] if result else (None)
    
    def get_all_users(self):
        self.c.execute(f"SELECT {self.user_id} FROM {self.USER_INFO}")
        results = self.c.fetchall()        
        self.conn.commit()
        return results

    def count_users(self):
        self.c.execute(f"SELECT COUNT({self.user_id}) FROM {self.USER_INFO}")
        row_count = self.c.fetchone()[0]
        return row_count   
        
    def delete_ids_from_file(self, filename):
            file = open(filename, "r")
            lines = file.readlines()
            ids_to_delete = []
            for line in lines:
                line = line.strip()
                ids_to_delete.append(int(line))
            file.close()
            sql = f"DELETE FROM {self.USER_INFO} WHERE {self.user_id} IN (%s)" % ",".join("?" * len(ids_to_delete))
            self.c.execute(sql, ids_to_delete)
            count = self.c.rowcount
            self.conn.commit()
            return f"{count} record(s) deleted"
    
    async def users_ids(self):
        self.c.execute(f"CREATE TEMPORARY TABLE temp_user_info AS SELECT * FROM {self.USER_INFO}")

        self.c.execute(f"SELECT {self.user_id} FROM temp_user_info")
        while True:
            user_id = self.c.fetchone()
            if user_id is None:
                break
            yield user_id

        self.c.execute("DROP TABLE temp_user_info")

    def delate_ids(self, user_id):
        self.c.execute(f"DELETE FROM {self.USER_INFO} WHERE {self.user_id} = ?", (user_id,)) 
        self.conn.commit()
        return f"Deleted"
    
    def insert_steem_username(self, steem_username):
        self.c.execute(f"INSERT OR REPLACE INTO {self.STEEM_USER} ({self.steem_username}, {self.steem_post}, {self.post_date})  VALUES (?, ?, ?)", (steem_username, None, None))
        self.conn.commit()

    def update_steem_post_and_date(self, username, new_post, new_date):
        self.c.execute(f'''
            UPDATE {self.STEEM_USER}
            SET {self.steem_post} = ?, {self.post_date} = ?
            WHERE {self.steem_username} = ?
        ''', (new_post, new_date, username))
        self.conn.commit()

    def get_user_steem_post(self, steem_username):
        self.c.execute(f'''SELECT {self.steem_post} FROM {self.STEEM_USER} WHERE {self.steem_username} = ?''', (steem_username,))
        result = self.c.fetchone()
        self.conn.commit()
        return result[0] if result else (None)

    def delate_steem_user(self, user_ids):
        for user_id in user_ids:
            self.c.execute(f"DELETE FROM {self.STEEM_USER} WHERE {self.user_id} = ?", (user_id,)) 
        self.conn.commit()          
    
    def get_steem_user(self, user_id):
        self.c.execute(f'''SELECT {self.steem_username} FROM {self.STEEM_USER} WHERE {self.user_id} = ?''', (user_id,))
        result = self.c.fetchone()
        self.conn.commit()
        return result[0] if result else (None)
    
    async def steem_usernames(self):
        # self.c.execute(f"CREATE TEMPORARY TABLE IF NOT EXISTS temp_steem_user AS SELECT * FROM {self.STEEM_USER}")

        # self.c.execute(f"SELECT {self.steem_username} FROM temp_steem_user")
        self.c.execute(f"SELECT {self.steem_username} FROM {self.STEEM_USER}")
        results = self.c.fetchall()
        for result in results:
            yield result[0]

    def count_steem_users(self):
        self.c.execute(f"SELECT COUNT({self.steem_username}) FROM {self.STEEM_USER}")
        row_count = self.c.fetchone()[0]
        return row_count   
    
    def insert_user_channel(self, channel_id, user_id):
        self.c.execute(f"INSERT OR REPLACE INTO {self.USER_CHANNEL} ({self.channel_id}, {self.user_id}) VALUES (?, ?)", (channel_id, user_id))
        self.conn.commit()

    def delate_channel_id(self, channel_id):
        self.c.execute(f"DELETE FROM {self.USER_CHANNEL} WHERE {self.channel_id} = ?", (channel_id,)) 
        self.conn.commit()
        return f"Deleted"
    
    def get_all_channel_user(self, user_id):
        self.c.execute(f'''SELECT {self.channel_id} FROM {self.USER_CHANNEL} WHERE {self.user_id} = ?''', (user_id,))
        results = self.c.fetchall()        
        self.conn.commit()
        return results