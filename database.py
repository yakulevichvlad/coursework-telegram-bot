"""
SQLite Database Setup with SQLAlchemy ORM
Defines models for User, Coursework, Topic, Chapter, and Reference entities.
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from typing import Optional

# Database configuration
DATABASE_URL = "sqlite:///./coursework_bot.db"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()


# Association table for many-to-many relationship between Coursework and Topic
coursework_topic_association = Table(
    'coursework_topic',
    Base.metadata,
    Column('coursework_id', Integer, ForeignKey('coursework.id'), primary_key=True),
    Column('topic_id', Integer, ForeignKey('topic.id'), primary_key=True)
)

# Association table for many-to-many relationship between Chapter and Reference
chapter_reference_association = Table(
    'chapter_reference',
    Base.metadata,
    Column('chapter_id', Integer, ForeignKey('chapter.id'), primary_key=True),
    Column('reference_id', Integer, ForeignKey('reference.id'), primary_key=True)
)


class User(Base):
    """
    User model to store Telegram user information.
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, index=True, nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    courseworks = relationship("Coursework", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username='{self.username}')>"


class Coursework(Base):
    """
    Coursework model to store coursework projects.
    """
    __tablename__ = "coursework"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="draft", index=True)  # draft, in_progress, completed
    progress_percentage = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deadline = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="courseworks")
    topics = relationship(
        "Topic",
        secondary=coursework_topic_association,
        back_populates="courseworks"
    )
    chapters = relationship("Chapter", back_populates="coursework", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Coursework(id={self.id}, title='{self.title}', status='{self.status}')>"


class Topic(Base):
    """
    Topic model to categorize coursework topics.
    """
    __tablename__ = "topic"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    courseworks = relationship(
        "Coursework",
        secondary=coursework_topic_association,
        back_populates="topics"
    )

    def __repr__(self):
        return f"<Topic(id={self.id}, name='{self.name}')>"


class Chapter(Base):
    """
    Chapter model to structure coursework into chapters.
    """
    __tablename__ = "chapter"

    id = Column(Integer, primary_key=True, index=True)
    coursework_id = Column(Integer, ForeignKey("coursework.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    order = Column(Integer, nullable=False)  # Chapter order within coursework
    status = Column(String(50), default="pending", index=True)  # pending, in_progress, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    coursework = relationship("Coursework", back_populates="chapters")
    references = relationship(
        "Reference",
        secondary=chapter_reference_association,
        back_populates="chapters"
    )

    def __repr__(self):
        return f"<Chapter(id={self.id}, title='{self.title}', order={self.order})>"


class Reference(Base):
    """
    Reference model to store citations and references for coursework.
    """
    __tablename__ = "reference"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    authors = Column(String(500), nullable=True)
    source_url = Column(String(500), nullable=True)
    publication_year = Column(Integer, nullable=True)
    reference_type = Column(String(50), nullable=False)  # book, article, website, etc.
    citation_format = Column(Text, nullable=True)  # APA, MLA, Chicago, etc.
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chapters = relationship(
        "Chapter",
        secondary=chapter_reference_association,
        back_populates="references"
    )

    def __repr__(self):
        return f"<Reference(id={self.id}, title='{self.title}', type='{self.reference_type}')>"


def init_db():
    """
    Initialize the database by creating all tables.
    Call this function once at application startup.
    """
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")


def get_db():
    """
    Dependency function to get a database session.
    Use this in your application to get a session for database operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    # Initialize database when script is run directly
    init_db()
