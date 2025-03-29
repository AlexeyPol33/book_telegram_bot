import sys
import asyncio

from sqlalchemy import Column, Integer, BigInteger, \
ForeignKey, String, Double, DateTime, Text, Table, LargeBinary
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.asyncio import create_async_engine

Base = declarative_base()

book_author = Table('book_authors', Base.metadata,
    Column('author_id', Integer, ForeignKey('authors.id')),
    Column('book_id', Integer, ForeignKey('books.id')))


book_category = Table('book_categories', Base.metadata,
    Column('category_id', Integer, ForeignKey('categories.id')),
    Column('book_id', Integer, ForeignKey('books.id')))


book_genre = Table('book_genres', Base.metadata,
    Column('genre_id', Integer, ForeignKey('genres.id')),
    Column('book_id', Integer, ForeignKey('books.id')))

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, autoincrement=True, primary_key=True)
    extension = Column(String(5))
    content = Column(LargeBinary)
    book = relationship("Book", back_populates="file", uselist=False)


class BookName(Base):
    __tablename__ = 'books_names'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, unique=True)
    book = relationship("Book", back_populates="name", uselist=False)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text)
    books = relationship('Book', secondary=book_category, back_populates='categories')

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text)
    books = relationship('Book', secondary=book_genre, back_populates='genres')

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, unique=True)
    books = relationship('Book', secondary=book_author, back_populates='authors')


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = relationship('BookName', back_populates='book', uselist=False)
    authors = relationship('Author',secondary=book_author, back_populates='books')
    categories = relationship('Category', secondary=book_category, back_populates='books')
    genres = relationship('Genre', secondary=book_genre, back_populates='books')
    description = Column(Text)
    file = relationship('File', uselist=False)


async def create_tables():
    engine = create_async_engine('postgresql+asyncpg://postgres:postgres@localhost/books')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(create_tables())