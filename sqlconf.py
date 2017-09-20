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
        tblitemsstmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text,count integer)"
        itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)"
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
        tblopstmt = "CREATE TABLE IF NOT EXISTS operator_client (operator text, owner text)"
        opidx="CREATE INDEX IF NOT EXISTS ownIndex ON operator_client (operator ASC)"
        clientidx="CREATE INDEX IF NOT EXISTS ownIndex ON operator_client (owner ASC)"
        self.conn.execute(tblitemsstmt)
        self.conn.execute(itemidx)
        self.conn.execute(ownidx)
        self.conn.execute(tblopstmt)
        self.conn.execute(opidx)
        self.conn.execute(clientidx)
        self.conn.commit()

    def add_item(self, item_text, owner):
        stmt = "INSERT INTO items (description, owner,count) VALUES (?, ?,1)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def add_operator(self, operator):
        stmt = "INSERT INTO operator_client (operator,owner) VALUES (?,'')"
        args = (operator,)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def update_operator(self, operator, owner):
        stmt = "Update operator_client set owner = (?) where operator = (?)"
        args = (owner,operator)
        self.conn.execute(stmt, args)
        self.conn.commit()


    def delete_operator(self, operator):
        stmt = "Delete from operator_client where operator = (?)"
        args = (operator,)
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
    def get_countforitem(self, description):
        stmt = "SELECT count FROM items WHERE description = (?)"
        args = (description,)
        return [x[0] for x in self.conn.execute(stmt, args)]

    def get_operators(self, operator):
        stmt = "SELECT operator FROM operator_client WHERE operator = (?)"
        args = (operator,)
        return [x[0] for x in self.conn.execute(stmt, args)]

    def get_client(self, operator):
        stmt = "SELECT owner FROM operator_client WHERE operator = (?)"
        args = (operator,)
        return [x[0] for x in self.conn.execute(stmt, args)]
    def get_operator(self, client):
        stmt = "SELECT operator FROM operator_client WHERE owner = (?)"
        args = (client,)
        return [x[0] for x in self.conn.execute(stmt, args)]

    def get_top5words(self, operator):
        stmt = "SELECT description FROM items WHERE owner in (select owner from operator_client where operator = (?)) order by count DESC Limit 5"
        args = (operator,)
        return [x[0] for x in self.conn.execute(stmt, args)]

    def get_freeoperator(self):
        stmt = "SELECT operator FROM operator_client WHERE owner = '' Limit 1"
        return [x[0] for x in self.conn.execute(stmt)]
