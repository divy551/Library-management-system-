"""
Loans app views - Book borrowing endpoints.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg import openapi
from .models import Loan
from .serializers import LoanSerializer, LoanDetailSerializer, BorrowBookSerializer, EmptySerializer
from apps.books.models import Book
from apps.accounts.permissions import IsAdministrator, IsOwnerOrAdministrator


class LoanViewSet(viewsets.ModelViewSet):
    """
    Book Loan Management API
    
    Members: Borrow books, view loans
    Administrators: Manage all loans
    """
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']
    filter_backends = []
    pagination_class = None

    def get_queryset(self):
        """Filter loans by user role."""
        user = self.request.user
        queryset = Loan.objects.select_related('user', 'book')
        
        if getattr(self, 'swagger_fake_view', False):
            return Loan.objects.none()
        
        if user.groups.filter(name='Administrators').exists():
            return queryset.order_by('-borrowed_at')
        return queryset.filter(user=user).order_by('-borrowed_at')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LoanDetailSerializer
        return LoanSerializer

    @swagger_auto_schema(
        operation_id="ListLoans",
        operation_summary="List loans",
        operation_description="Administrators see all loans, members see own loans.",
        responses={200: LoanSerializer(many=True)},
        manual_parameters=[]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="CreateLoanManual",
        operation_summary="Create Loan (Manual)",
        operation_description="Manually create a loan record (Alternative to Checkout)"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="GetLoan",
        operation_summary="Get loan details",
        operation_description="Retrieve a specific loan by ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="CheckoutBook",
        operation_summary="Checkout book",
        operation_description="Borrow a book from the library",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['book_id'],
            properties={
                'book_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Book ID to borrow')
            }
        ),
        responses={
            201: LoanSerializer,
            400: "Book unavailable or limit reached"
        }
    )
    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """Borrow a book by ID."""
        serializer = BorrowBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_id = serializer.validated_data['book_id']

        with transaction.atomic():
            try:
                book = Book.objects.select_for_update().get(pk=book_id)
            except Book.DoesNotExist:
                return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)

            if not book.is_available:
                return Response({'error': 'Book is not available.'}, status=status.HTTP_400_BAD_REQUEST)

            if Loan.objects.filter(user=request.user, book=book, returned_at__isnull=True).exists():
                return Response({'error': 'You already have this book.'}, status=status.HTTP_400_BAD_REQUEST)

            # Limit: 1 book at a time
            if Loan.objects.filter(user=request.user, returned_at__isnull=True).exists():
                return Response({'error': 'You can only borrow 1 book at a time.'}, status=status.HTTP_400_BAD_REQUEST)

            loan = Loan.objects.create(user=request.user, book=book)
            book.is_available = False
            book.save()

        return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_id="CheckinBook",
        operation_summary="Checkin book",
        operation_description="Process book return (Admin only)",
        request_body=no_body,
        responses={
            200: LoanSerializer,
            400: "Already returned",
            404: "Loan not found"
        }
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAdministrator])
    def checkin(self, request, pk=None):
        """Return a borrowed book (Admin only)."""
        loan = self.get_object()

        if loan.returned_at:
            return Response({'error': 'Book already returned.'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            loan.returned_at = timezone.now()
            loan.save()
            loan.book.is_available = True
            loan.book.save()

        return Response(LoanSerializer(loan).data)

    @swagger_auto_schema(
        operation_id="MyCurrentLoans",
        operation_summary="Current loans",
        operation_description="Get active (unreturned) loans"
    )
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get active loans."""
        queryset = self.get_queryset().filter(returned_at__isnull=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_id="ListAllLoansAdmin",
        operation_summary="All loans (Admin)",
        operation_description="View all system loans - admin only"
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAdministrator])
    def all_loans(self, request):
        """Get all loans (Admin only)."""
        queryset = Loan.objects.select_related('user', 'book').order_by('-borrowed_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_id="ListOverdueLoans",
        operation_summary="Overdue loans (Admin)",
        operation_description="View overdue loans - admin only"
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAdministrator])
    def overdue(self, request):
        """Get overdue loans (Admin only)."""
        queryset = Loan.objects.filter(
            returned_at__isnull=True,
            due_date__lt=timezone.now()
        ).select_related('user', 'book').order_by('-due_date')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_id="MyLoanHistory",
        operation_summary="Loan history",
        operation_description="Get all your loans including returned"
    )
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get user's loan history."""
        queryset = Loan.objects.filter(user=request.user).select_related('book').order_by('-borrowed_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
