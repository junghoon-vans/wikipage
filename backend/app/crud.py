from app import models
from app import schemas
from elasticsearch import Elasticsearch
from sqlalchemy.orm import Session


posts_index = "wiki.public.posts"

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


def get_post(es: Elasticsearch, post_id: int) -> models.Post:
    """
    Get a post from the database.
    :param es: elasticsearch session
    :param post_id: the id of the post to retrieve
    :return: the post if it exists
    """
    res = es.get(index=posts_index, id=post_id)
    return res["_source"]


def get_posts(es: Elasticsearch) -> list[schemas.PostList]:
    """
    Get all posts from the database.
    :param es: elasticsearch session
    :return: the posts
    """
    res = es.search(index=posts_index, query={"match_all": {}})
    return [schemas.PostList.model_validate(hit["_source"]) for hit in res["hits"]["hits"]]


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


def get_related_posts(es: Elasticsearch, post_id: int) -> list[schemas.PostList]:
    """
    Get related posts from the elasticsearch.

    :param es: elasticsearch session
    :param post_id: the id of the post to retrieve
    :return: the posts
    """
    posts_count = es.count(index=posts_index, body={"query": {"match_all": {}}})["count"]

    if (posts_count < 2):
        return []

    posts = _more_like_posts(es, post_id, round(posts_count * 0.6))

    if (posts['hits']['total']['value'] == 0):
        return []

    total_terms = []
    for post in posts['hits']['hits']:
        total_terms += post['_source']['content'].split()
    
    # Filter out terms that appear in more than 40% of the total terms
    total_terms = list(filter(lambda x: total_terms.count(x) <= posts_count * 0.4, total_terms))

    # Filter out terms that appear in the current post
    current_post = es.get(index=posts_index, id=post_id)['_source']
    current_post_terms = set(current_post['content'].split())
    terms = list(filter(lambda x: x in current_post_terms, total_terms))

    res = _get_posts_with_terms(es, post_id, set(terms), 2)

    return [schemas.PostList.model_validate(hit["_source"]) for hit in res["hits"]["hits"]]


def _more_like_posts(es: Elasticsearch, id: int, max_doc_freq: int):
    """
    Get posts that are more like the post with the given id from the elasticsearch.

    :param es: elasticsearch session
    :param id: the id of the post to retrieve
    :param max_doc_freq: the max doc freq to match
    """
    return es.search(
        index=posts_index,
        body={
            "query": {
                "more_like_this": {
                    "fields": ["content"],
                    "like": [
                        {
                            "_id": id,
                        },
                    ],
                    "min_term_freq": 1,
                    "min_doc_freq": 1,
                    "max_doc_freq": round(max_doc_freq),
                },
            },
        },
    )


def _get_posts_with_terms(es: Elasticsearch, id: int, terms: set[str], match_count: int):
    """
    Get posts with terms from the elasticsearch.
    
    :param es: elasticsearch session
    :param id: the id of the post to retrieve
    :param terms: the terms to match
    :param match_count: the number of terms to match
    """
    return es.search(
        index=posts_index, body={
            "query": {
                "bool": {
                    "should": [{"match": {"content": term}} for term in terms],
                    "minimum_should_match": match_count,
                    "must_not": [
                        {
                            "ids": {
                                "values": [id],
                            },
                        },
                    ],
                },
            },
            "sort": [
                {"_score": {"order": "desc"}},
            ],
        },
    )
