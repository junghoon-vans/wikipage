from typing import List, Type

from sqlalchemy.orm import Session

from . import models
from . import schemas
from .models import Post


def create_post(db: Session, post: schemas.PostCreate) -> models.Post:
    """
    Create a new post in the database.
    :param db: database session
    :param post: post data
    :return: the newly created post
    """
    db_post = models.Post(title=post.title, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_post(db: Session, post_id: int) -> models.Post:
    """
    Get a post from the database.
    :param db: database session
    :param post_id: the id of the post to retrieve
    :return: the post if it exists
    """
    return db.query(models.Post).get(post_id)


def get_posts(db: Session) -> list[Type[Post]]:
    """
    Get all posts from the database.
    :param db: database session
    :return: the posts
    """
    return db.query(models.Post).all()


def update_post(db: Session, post_id: int, post: schemas.PostCreate) -> models.Post:
    """
    Update a post in the database.
    :param db: database session
    :param post_id: the id of the post to update
    :param post: the post data
    :return: the updated post
    """
    db_post = db.query(models.Post).get(post_id)
    db_post.title = post.title
    db_post.content = post.content
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int) -> models.Post:
    """
    Delete a post from the database.
    :param db: database session
    :param post_id: the id of the post to delete
    :return: the deleted post if it existed
    """
    db_post = db.query(models.Post).get(post_id)
    db.delete(db_post)
    db.commit()
    return db_post