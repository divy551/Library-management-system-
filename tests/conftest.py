"""
Pytest configuration and fixtures.
"""
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import Group
from apps.accounts.models import User
from apps.books.models import Book


@pytest.fixture
def api_client():
    """Return an API client for making requests."""
    return APIClient()


@pytest.fixture
def admin_group(db):
    """Create and return the Administrators group."""
    group, _ = Group.objects.get_or_create(name='Administrators')
    return group


@pytest.fixture
def member_group(db):
    """Create and return the Members group."""
    group, _ = Group.objects.get_or_create(name='Members')
    return group


@pytest.fixture
def admin_user(db, admin_group):
    """Create and return an administrator user."""
    user = User.objects.create_user(
        email='admin@library.com',
        username='admin',
        password='AdminPass123!'
    )
    user.groups.add(admin_group)
    return user


@pytest.fixture
def member_user(db, member_group):
    """Create and return a member user."""
    user = User.objects.create_user(
        email='member@library.com',
        username='member',
        password='MemberPass123!'
    )
    user.groups.add(member_group)
    return user


@pytest.fixture
def another_member_user(db, member_group):
    """Create and return another member user."""
    user = User.objects.create_user(
        email='another@library.com',
        username='another',
        password='AnotherPass123!'
    )
    user.groups.add(member_group)
    return user


@pytest.fixture
def authenticated_admin_client(admin_user):
    """Return an API client authenticated as admin."""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def authenticated_member_client(member_user):
    """Return an API client authenticated as member."""
    client = APIClient()
    client.force_authenticate(user=member_user)
    return client


@pytest.fixture
def sample_book(db):
    """Create and return a sample available book."""
    return Book.objects.create(
        title='Clean Code',
        author='Robert C. Martin',
        isbn='9780132350884',
        description='A handbook of agile software craftsmanship',
        page_count=464,
        genre='Programming',
        is_available=True
    )


@pytest.fixture
def another_book(db):
    """Create and return another sample book."""
    return Book.objects.create(
        title='Design Patterns',
        author='Erich Gamma',
        isbn='9780201633610',
        description='Elements of Reusable Object-Oriented Software',
        page_count=395,
        genre='Programming',
        is_available=True
    )


@pytest.fixture
def unavailable_book(db):
    """Create and return an unavailable book."""
    return Book.objects.create(
        title='Refactoring',
        author='Martin Fowler',
        isbn='9780201485677',
        description='Improving the Design of Existing Code',
        page_count=431,
        genre='Programming',
        is_available=False
    )
