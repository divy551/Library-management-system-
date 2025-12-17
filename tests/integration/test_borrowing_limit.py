import pytest
from django.urls import reverse
from apps.books.models import Book

@pytest.mark.django_db
class TestCheckoutLimit:
    """Test the 1-book checkout limit per user."""

    def test_cannot_checkout_more_than_one_book(self, authenticated_member_client, authenticated_admin_client, sample_book):
        """
        Verify that a user cannot checkout a second book while having an active loan.
        """
        # Create a second book
        second_book = Book.objects.create(
            title="Second Book",
            author="Author Two",
            isbn="9876543210123",
            page_count=200,
            is_available=True
        )

        checkout_url = reverse('loan-checkout')

        # 1. Checkout first book (Should Succeed)
        response1 = authenticated_member_client.post(checkout_url, {'book_id': sample_book.id})
        assert response1.status_code == 201, "First checkout should succeed"

        # 2. Try to checkout second book (Should Fail)
        response2 = authenticated_member_client.post(checkout_url, {'book_id': second_book.id})
        assert response2.status_code == 400, "Second checkout should fail due to limit"
        assert "only borrow 1 book" in str(response2.data['error'])

        # 3. Checkin first book (Using Admin client)
        loan_id = response1.data['id']
        checkin_url = reverse('loan-checkin', args=[loan_id])
        
        checkin_response = authenticated_admin_client.post(checkin_url)
        assert checkin_response.status_code == 200, "Admin should be able to checkin book"

        # 4. Checkout second book again (Should Succeed now)
        response3 = authenticated_member_client.post(checkout_url, {'book_id': second_book.id})
        assert response3.status_code == 201, "After checkin, checkout should succeed"
