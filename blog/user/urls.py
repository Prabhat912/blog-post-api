"""
URL mappings for the user API.
"""
from django.urls import path
from graphene_django.views import GraphQLView
from user import schema


app_name = 'user'

urlpatterns = [
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
]
