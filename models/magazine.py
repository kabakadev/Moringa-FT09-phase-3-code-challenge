from database.connection import get_db_connection
class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self,id):
        if type(id) is int:
            self._id = id
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,name):
        if isinstance(name,str) and 2 <= len(name) <=16:
            self._name = name
        else:
            raise ValueError("Name must be a string between 2 and 16 characters")
    @property
    def category(self):
        return self._category
    @category.setter
    def category(self,category):
        if isinstance(category,str) and len(category):
            self._category = category
        else:
            raise ValueError('Category must be a non empty string')

    def __repr__(self):
        return f'<Magazine {self.name}>'
    def articles(self):
        from models.article import Article
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        sql = """
            SELECT * FROM articles
            INNER JOIN magazines 
            ON magazines.id = articles.magazine_id
            WHERE magazines.id = ?
            """
        CURSOR.execute(sql,(self.id,))
        rows = CURSOR.fetchall()
        CONN.close()
        return [Article(row["id"], row["title"], row["content"],row["author_id"],row["magazine_id"]) for row in rows]
    def contributors(self):
        from models.author import Author
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        sql = """
            SELECT DISTINCT authors.* FROM authors
            INNER JOIN articles
            ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
            """
        CURSOR.execute(sql,(self.id,))
        rows = CURSOR.fetchall()
        CONN.close()
        return [Author(row["id"],row["name"]) for row in rows ]
    def article_titles(self):
        """returns a list of titles strings of all articles written for that magazine"""
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        sql = """
            SELECT articles.title FROM articles
            INNER JOIN magazines 
            ON magazines.id = articles.magazine_id
            WHERE magazines.id = ?
            """
        CURSOR.execute(sql,(self.id,))
        rows = CURSOR.fetchall()

        if not rows:
            return None
        return [row["title"] for row in rows]
    def contributing_authors(self):
        """returns a list of authors who have written more than 2 articles for the magazine"""
        from models.author import Author
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        sql = """
            SELECT authors.name,authors.id FROM authors
            INNER JOIN articles 
            ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id,authors.name
            HAVING COUNT(articles.id) >2
            """
        CURSOR.execute(sql,(self.id,))
        rows = CURSOR.fetchall()

        if not rows:
            return None
        return [Author(row["id"],row["name"]) for row in rows]



    
    

