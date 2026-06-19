from abc import ABC, abstractmethod
from db.connection import DatabaseManager
from db.models import Snippet

class BaseSnippetRepository(ABC):
    """Abstract interface contract for snippet data source operations."""
    
    @abstractmethod
    def add(self, snippet: Snippet):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def delete(self, snippet_id: int):
        pass

    @abstractmethod
    def update_category(self, snippet_id: int, category: str):
        pass

    @staticmethod
    def get_existing_categories(snippets):
        """Helper to extract distinct category names from a list of Snippet instances."""
        cats = set()
        for s in snippets:
            if s.category:
                cats.add(s.category.strip())
        cats.add("Uncategorized")
        return sorted(list(cats))


class SQLSnippetRepository(BaseSnippetRepository):
    """Concrete SQL implementation of the snippet repository interface, compatible with SQLite and PostgreSQL."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def add(self, snippet: Snippet):
        conn = self.db_manager.get_connection()
        c = conn.cursor()
        p = self.db_manager.placeholder
        c.execute(
            f"INSERT INTO snippets (title, content, description, tags, type, language, category) VALUES ({p}, {p}, {p}, {p}, {p}, {p}, {p})",
            (snippet.title, snippet.content, snippet.description, snippet.tags_csv, snippet.type, snippet.language, snippet.category)
        )
        conn.commit()
        conn.close()

    def get_all(self):
        conn = self.db_manager.get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM snippets ORDER BY created_at DESC")
        columns = [col[0] for col in c.description]
        rows = c.fetchall()
        conn.close()
        
        # Convert tuples to Snippet data model instances
        return [Snippet.from_db_row(row, columns) for row in rows]

    def delete(self, snippet_id: int):
        conn = self.db_manager.get_connection()
        c = conn.cursor()
        p = self.db_manager.placeholder
        c.execute(f"DELETE FROM snippets WHERE id = {p}", (snippet_id,))
        conn.commit()
        conn.close()

    def update_category(self, snippet_id: int, category: str):
        conn = self.db_manager.get_connection()
        c = conn.cursor()
        p = self.db_manager.placeholder
        c.execute(f"UPDATE snippets SET category = {p} WHERE id = {p}", (category, snippet_id))
        conn.commit()
        conn.close()


