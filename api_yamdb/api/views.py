from rest_framework import viewsets, status, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins
from django.shortcuts import get_object_or_404

class ReviewViewSet(viewsets.ModelViewSet):
    """
    Api endpoint has access to SAFE_METHODS
    without registering.
    """
    pass
    #serializer_class = ReviewSerializer


    '''def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        return title.review.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user,
                        title_id=title)'''


class CommentViewSet(viewsets.ModelViewSet):
    """
    Api endpoint has access to SAFE_METHODS
    without registering.
    """
    pass
    '''serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user,
                        post=post)'''