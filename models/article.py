from models.author import Author

from database.connection import get_db_connection
class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f'<Article {self.title}>'
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self,title):
        if hasattr(self,'_title'):
            raise AttributeError("Title cannot be changed after the article is instantiated")
        if type(title) is str and 5 <= len(title) <= 50:
            self._title = title
        else:
            raise ValueError("Pass a valid integer value")
    @property
    def author(self):
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        sql = """
            SELECT authors.id, authors.name
            FROM authors
            INNER JOIN articles ON authors.id = articles.author_id
            WHERE articles.id = ?
            """
        CURSOR.execute(sql,(self.id,))
        row = CURSOR.fetchone()
        CONN.close()
    
        return Author(row["id"],row["name"]) if row else None 
    @property
    def magazine(self):
        from magazine import Magazine
        CONN = get_db_connection()
        CURSOR = CONN.cursor()
        sql = """
            SELECT magazines.id, magazines.name,magazines.category
            FROM magazines
            INNER JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.id = ?
            """
        CURSOR.execute(sql,(self.id,))
        row = CURSOR.fetchone()
        CONN.close()
        
        return Magazine(row["id"],row["name"],row["category"] ) if row else None 
