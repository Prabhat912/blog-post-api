import graphene
# from graphene import relay, ObjectType
from graphene_django.types import DjangoObjectType
# from graphene_django.filter import DjangoFilterConnectionField
# from django.contrib.auth import get_user_model
# from graphene_django.forms.mutation import DjangoModelFormMutation
from core.models import BlogPost


class BlogPostType(DjangoObjectType):
    class Meta:
        model = BlogPost


class Query(graphene.ObjectType):
    all_blog_posts = graphene.List(BlogPostType)
    blog_post = graphene.Field(BlogPostType, id=graphene.Int())

    def resolve_all_blog_posts(self, info):
        return BlogPost.objects.all()

    def resolve_blog_post(self, info, id):
        try:
            return BlogPost.objects.get(pk=id)
        except BlogPost.DoesNotExist:
            return None


class CreateBlogPost(graphene.Mutation):
    blog_post = graphene.Field(BlogPostType)

    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    # @login_required
    def mutate(self, info, title, content):
        user = info.context.user
        blog_post = BlogPost(title=title, content=content, author_id=user)
        blog_post.save()
        return CreateBlogPost(blog_post=blog_post)


class UpdateBlogPost(graphene.Mutation):
    blog_post = graphene.Field(BlogPostType)

    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        content = graphene.String()

    # @login_required
    def mutate(self, info, id, title=None, content=None):
        user = info.context.user
        try:
            blog_post = BlogPost.objects.get(pk=id, author_id=user)
        except BlogPost.DoesNotExist:
            raise Exception("Blog post not found or you don't have permission \
                             to edit it")

        if title is not None:
            blog_post.title = title
        if content is not None:
            blog_post.content = content
        blog_post.save()
        return UpdateBlogPost(blog_post=blog_post)


class DeleteBlogPost(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    # @login_required
    def mutate(self, info, id):
        user = info.context.user
        try:
            blog_post = BlogPost.objects.get(pk=id, author_id=user)
            blog_post.delete()
            return DeleteBlogPost(success=True)
        except BlogPost.DoesNotExist:
            raise Exception("Blog post not found or you don't \
                            have permission to delete it")


class Mutation(graphene.ObjectType):
    create_blog_post = CreateBlogPost.Field()
    update_blog_post = UpdateBlogPost.Field()
    delete_blog_post = DeleteBlogPost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
