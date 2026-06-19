from datetime import datetime


class Snippet:
    def __init__(
        self,
        id_val,
        title,
        content,
        description,
        tags,
        snippet_type,
        language,
        category,
        created_at=None,
    ):
        self.id = id_val
        self.title = title
        self.content = content
        self.description = description

        # Tags can be passed as a list or a comma-separated string
        if isinstance(tags, list):
            self.tags = [t.strip() for t in tags if t.strip()]
        else:
            self.tags = [t.strip() for t in (tags or "").split(",") if t.strip()]

        self.type = snippet_type  # 'Code' or 'Command'
        self.language = language
        self.category = category or "Uncategorized"
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def tags_csv(self):
        """Returns the tags as a comma-separated string for DB storage."""
        return ",".join(self.tags)

    @classmethod
    def from_db_row(cls, row, columns):
        """Factory method to construct a Snippet instance from an SQL row tuple."""
        row_dict = dict(zip(columns, row))
        return cls(
            id_val=row_dict.get("id"),
            title=row_dict.get("title"),
            content=row_dict.get("content"),
            description=row_dict.get("description"),
            tags=row_dict.get("tags"),
            snippet_type=row_dict.get("type"),
            language=row_dict.get("language"),
            category=row_dict.get("category"),
            created_at=row_dict.get("created_at"),
        )
