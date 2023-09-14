"""
Schema for Users
"""
import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model
from graphene import InputObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude = ('password', 'is_superuser')


class UserInput(InputObjectType):
    username = graphene.String()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        user_data = UserInput(required=True)

    def mutate(self, info, email, password, user_data):
        user = get_user_model()(
            email=email,
            **user_data
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        user_data = UserInput(required=True)

    def mutate(self, info, user_data):
        user = info.context.user
        if user.is_authenticated:
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()
            return UpdateUser(user=user)
        return UpdateUser(user=None)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        return None


schema = graphene.Schema(query=Query, mutation=Mutation)
