from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import CommentSerializer, ReviewGetSerializer, ReviewPostSerializer
from review.models import Review, TITLES


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Api endpoint has access to SAFE_METHODS
    without registering.
    """
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(TITLES, pk=title_id)
        return title.review_title.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReviewGetSerializer
        return ReviewPostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    Api endpoint has access to SAFE_METHODS
    without registering.
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        review = Review.objects.get(pk=review_id,
                                    title_id=title_id)
        return review.review_comment.all()
