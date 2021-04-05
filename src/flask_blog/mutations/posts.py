import graphene
from graphene import relay
from graphql import GraphQLError

from .. import models, types
from ..database import db
from ..utils import find_or_create_tags


class CreatePostInput:
    title = graphene.String(required=True)
    content = graphene.String(required=True)
    tags = graphene.String(required=False)


class CreatePostSuccess(graphene.ObjectType):
    post = graphene.Field(types.PostNode, required=True)


class CreatePostOutput(graphene.Union):
    class Meta:
        types = (CreatePostSuccess,)


class CreatePost(relay.ClientIDMutation):
    Input = CreatePostInput
    Output = CreatePostOutput

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        input['tags'] = find_or_create_tags(input['tags'])
        new_post = models.Post(**input)
        db.session.add(new_post)
        db.session.commit()

        return CreatePostSuccess(post=new_post)


class DeletePostInput:
    postId = graphene.ID(required=True)


class DeletePostSuccess(graphene.ObjectType):
    post = graphene.Field(types.PostNode, required=True)


class DeletePostOutput(graphene.Union):
    class Meta:
        types = (DeletePostSuccess,)


class DeletePost(relay.ClientIDMutation):
    Input = DeletePostInput
    Output = DeletePostOutput

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        post = models.Post.query.get(input['postId'])
        if post is None:
            raise GraphQLError('That post does not exist')
        db.session.delete(post)
        db.session.commit()

        return DeletePostSuccess(post=post)


class EditPostInput:
    postId = graphene.ID(required=True)
    title = graphene.String(required=False)
    content = graphene.String(required=False)
    tags = graphene.String(required=False)


class EditPostSuccess(graphene.ObjectType):
    post = graphene.Field(types.PostNode, required=True)


class EditPostOutput(graphene.Union):
    class Meta:
        types = (EditPostSuccess,)


class EditPost(relay.ClientIDMutation):
    Input = EditPostInput
    Output = EditPostOutput

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        post = models.Post.query.get(input['postId'])
        if post is None:
            raise GraphQLError('That post does not exist')
        if input['tags'] is not None:
            tags = find_or_create_tags(input['tags'])
            post.tags = tags
        if input['title'] is not None:
            post.title = input['title']
        if input['content'] is not None:
            post.content = input['content']
        db.session.commit()

        return EditPostSuccess(post=post)
