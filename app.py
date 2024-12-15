from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database and create tables
    create_tables()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()


    '''
        The following is just for testing purposes, 
        you can modify it to meet the requirements of your implmentation.
    '''

    # Create an author
    cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
    author_id = cursor.lastrowid # Use this to fetch the id of the newly created author

    # Create a magazine
    cursor.execute('INSERT INTO magazines (name, category) VALUES (?,?)', (magazine_name, magazine_category))
    magazine_id = cursor.lastrowid # Use this to fetch the id of the newly created magazine

    # Create an article
    cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                   (article_title, article_content, author_id, magazine_id))
    article_id = cursor.lastrowid

    conn.commit()

    # Query the database for inserted records. 
    # The following fetch functionality should probably be in their respective models

    cursor.execute('SELECT * FROM magazines')
    magazines = [Magazine(magazine["id"], magazine["name"], magazine["category"]) for magazine in cursor.fetchall()]

    cursor.execute('SELECT * FROM authors')
    authors = [Author(author["id"], author["name"]) for author in cursor.fetchall()]

    cursor.execute('SELECT * FROM articles')
    articles = [Article(article["id"], article["title"], article["content"], article["author_id"], article["magazine_id"]) for article in cursor.fetchall()]


    conn.close()

    # Display results
    print("\nMagazines:")
    for magazine in magazines:
        print(magazine)
        # Test article_titles() method
        print("Article Titles:", magazine.article_titles())
        # Test contributing_authors() method
        contributors = magazine.contributing_authors()
        if contributors:
            print("Contributing Authors:", [str(author) for author in contributors])
        else:
            print("No contributing authors with more than 2 articles.")

    print("\nAuthors:")
    for author in authors:
        print(author)
         # Test articles() method
        print("Articles by Author:", [str(article) for article in author.articles()])
         # Test magazines() method
        print("Magazines by Author:", [str(magazine) for magazine in author.magazines()])

    print("\nArticles:")
    for article in articles:
        print(article)

if __name__ == "__main__":
    main()
