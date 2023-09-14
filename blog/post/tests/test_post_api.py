# from django.test import TestCase
from graphene.test import Client
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
from core.models import BlogPost
from ..schema import schema


class BlogAPITestCase(JSONWebTokenTestCase):
    def setUp(self):
        self.client = Client(schema)
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="testpassword"
        )
        self.token = self.get_token(self.user)
        self.auth_headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

    def test_create_blog_post(self):
        mutation = '''
            mutation {
                createBlogPost(title: "Test Post", content: "Test content") {
                    blogPost {
                        id
                        title
                        content
                    }
                }
            }
        '''

        response = self.client.execute(mutation, headers=self.auth_headers)
        data = response.get('data', {})
        blog_post = data.get('createBlogPost', {}).get('blogPost', {})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(blog_post)
        self.assertEqual(blog_post['title'], "Test Post")
        self.assertEqual(blog_post['content'], "Test content")

    def test_edit_blog_post(self):
        blog_post = BlogPost.objects.create(
            title="Original Title",
            content="Original content",
            author_id=self.user
        )
        mutation = f'''
            mutation {{
                updateBlogPost(id: {blog_post.id}, title: "Updated Title",\
                     content: "Updated content") {{
                    blogPost {{
                        id
                        title
                        content
                    }}
                }}
            }}
        '''

        response = self.client.execute(mutation, headers=self.auth_headers)
        data = response.get('data', {})
        blog_post = data.get('updateBlogPost', {}).get('blogPost', {})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(blog_post)
        self.assertEqual(blog_post['title'], "Updated Title")
        self.assertEqual(blog_post['content'], "Updated content")

    def test_delete_blog_post(self):
        blog_post = BlogPost.objects.create(
            title="To Be Deleted",
            content="Delete this post",
            author=self.user
        )
        mutation = f'''
            mutation {{
                deleteBlogPost(id: {blog_post.id}) {{
                    success
                }}
            }}
        '''

        response = self.client.execute(mutation, headers=self.auth_headers)
        data = response.get('data', {})
        delete_result = data.get('deleteBlogPost', {})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(delete_result['success'])

    def test_view_all_blog_posts(self):
        # Create some sample blog posts
        BlogPost.objects.create(
            title="Post 1",
            content="Content for post 1",
            author=self.user
        )
        BlogPost.objects.create(
            title="Post 2",
            content="Content for post 2",
            author=self.user
        )

        query = '''
            query {
                allBlogPosts {
                    id
                    title
                    content
                }
            }
        '''

        response = self.client.execute(query)
        data = response.get('data', {})
        blog_posts = data.get('allBlogPosts', [])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(blog_posts), 2)

    def test_view_individual_blog_post(self):
        blog_post = BlogPost.objects.create(
            title="Individual Post",
            content="Content for individual post",
            author=self.user
        )

        query = f'''
            query {{
                blogPost(id: {blog_post.id}) {{
                    id
                    title
                    content
                }}
            }}
        '''

        response = self.client.execute(query)
        data = response.get('data', {})
        blog_post = data.get('blogPost', {})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(blog_post)
        self.assertEqual(blog_post['title'], "Individual Post")
        self.assertEqual(blog_post['content'], "Content for individual post")
