import sqlite3


class DBHelper:
    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def deletetable(self):
        tblstmt = "DROP TABLE items"
        self.conn.execute(tblstmt)
        self.conn.commit()

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text,count integer)"
        itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)"
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(itemidx)
        self.conn.execute(ownidx)
        self.conn.commit()

    def add_item(self, item_text, owner):
        stmt = "INSERT INTO items (description, owner,count) VALUES (?, ?,1)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def update_item(self, item_text, owner):
        stmt = "Update items set count=count+1 WHERE description = (?) AND owner = (?) "
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()
        stmt = "Select count from items WHERE description = (?) AND owner = (?)"
        return [x[0] for x in self.conn.execute(stmt, args)]

    def get_items(self, owner):
        stmt = "SELECT description FROM items WHERE owner = (?)"
        args = (owner,)
        return [x[0] for x in self.conn.execute(stmt, args)]
