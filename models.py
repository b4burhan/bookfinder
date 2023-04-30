from pydantic import BaseModel


class BookSchema(BaseModel):
    title: str
    publish_date: str
    author: str
    rating: int
    genre: str

    class Config:
        schema_extra = {
            "example": {
                "title": "Introduction to Programming",
                "publish_date": "2019-10-12",
                "author": "Deitel & Associates",
                "rating": 4,
                "genre": "programming",
            }
        }
