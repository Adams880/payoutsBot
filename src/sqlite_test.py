import sqlite3


class Event:
    members = []
    memberCount = 0
    time = ''
    date = ''

    def __init__(self, time, date):
        self.time = time
        self.date = date

    # def add_member(self, member: discord.Member):
    #     global members, memberCount
    #     members[memberCount] = member


conn = sqlite3.connect('botData.db')

c = conn.cursor()

event1 = Event('08:00AM', '07/11/1995')
event2 = Event('09:00PM', '05/10/1996')

# c.execute("""CREATE TABLE Servers(
# serverID TEXT PRIMARY KEY NOT NULL,
# name TEXT
# )""")

c.execute("INSERT INTO Servers VALUES (?, ?)", (event1.time, event1.date))

conn.commit()

c.execute("INSERT INTO Servers VALUES (:time, :date)", {'time': event2.time, 'date': event2.date})

conn.commit()

c.execute("SELECT * FROM Servers WHERE name=?", ('Bot Test Hangout',))

print(c.fetchall())

conn.commit()

conn.close()
