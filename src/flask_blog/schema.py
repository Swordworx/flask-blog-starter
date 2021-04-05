import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField

from . import models, mutations
from .types import PostConnection, TagConnection


postsArgs = {
    'tagName': graphene.String(required=False),
    'createdAt': graphene.String(required=False)
}


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    posts = SQLAlchemyConnectionField(PostConnection, **postsArgs)
    tags = SQLAlchemyConnectionField(TagConnection)

    def resolve_posts(self, info, *args, **kwargs):
        if 'tagName' in kwargs:
            tag_name = kwargs['tagName']
            query = SQLAlchemyConnectionField.get_query(models.Tag, info, *args)
            tag = query.filter(models.Tag.name == tag_name).first()
            return tag.posts if tag is not None else []
        query = SQLAlchemyConnectionField.get_query(
            models.Post, info, *args, **kwargs
        )
        if 'createdAt' in kwargs:
            created_at = kwargs['createdAt']
            query = query.filter(models.Post.created_at == created_at)
        return query.all()

    def resolve_tags(self, info, *args, **kwargs):
        query = SQLAlchemyConnectionField.get_query(
            models.Tag, info, *args, **kwargs
        )
        return query.all()


class Mutation(graphene.ObjectType):
    create_post = mutations.CreatePost.Field()
    edit_post = mutations.EditPost.Field()
    delete_post = mutations.DeletePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
