from database.connection import get_db_connection
class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self,id):
        if type(id) is int:
            self._id = id
        else:
            raise ValueError("Id must be an integer")
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,name):
        #Allow setting only if _name hasn't been set yet
        if hasattr(self,'_name'):
            raise AttributeError("Name cannot be changed after the author is instantiated")
        if type(name) is str and len(name) >0:
            self._name = name
        else:
            raise ValueError("Name must not be empty and be a valid string")

    def __repr__(self):
        return f'<Author {self.name}>'
    def articles(self):
        from models.article import Article
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        sql = """
        SELECT *
        FROM articles
        WHERE articles.author_id = ?
            """
        CURSOR.execute(sql,(self.id,))
        rows = CURSOR.fetchall()
        CONN.close()
        return [Article(row["id"], row["title"], row["content"], row["author_id"], row["magazine_id"]) for row in rows]

    def magazines(self):
        from models.magazine import Magazine
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        sql = """
        SELECT DISTINCT magazines.id,magazines.name,magazines.category
        FROM magazines
        INNER JOIN articles on magazines.id = articles.magazine_id
        WHERE articles.author_id = ?
            """
        CURSOR.execute(sql,(self.id,))
        rows = CURSOR.fetchall()
        CONN.close()
        return [Magazine(row["id"], row["name"], row["category"]) for row in rows]
       

