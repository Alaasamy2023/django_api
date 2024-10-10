# views.py
from rest_framework import generics
from .models import Post
from .serializers import PostSerializer




from .serializers import CreateUserSerializer, UserSerializer
from knox.models import AuthToken # type: ignore
from rest_framework.response import Response # type: ignore



from rest_framework import status # type: ignore
from django.contrib.auth.models import User, Group 
from rest_framework import viewsets, permissions, generics # type: ignore






# RegistrationAPI return all data
class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

















class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer



class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer










# ----------------------------
# الحذف فقط 

class PostDeleteAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticated]  # تحديد صلاحيات الوصول
    # لا تحتاج لدالة destroy() إلا إذا كنت بحاجة لتخصيص سلوك الحذف
    # يمكنك تعيين أي سلوك إضافي لعملية الحذف هنا

# ----------------------------
# ----------------------------



# ----------------------------
# لعرض كل البوست 

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        author_id = self.request.data.get('author_id')
        user = self.request.user
        
        if author_id:
            try:
                author = User.objects.get(id=author_id)
            except User.DoesNotExist:
                return Response({"error": "Invalid author ID provided."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            author = user if user.is_authenticated else None

        if author:
            serializer.save(author=author, author_id=author.id)
        else:
            return Response({"error": "You must provide a valid author ID or be authenticated to create a post."}, status=status.HTTP_403_FORBIDDEN)

    def perform_update(self, serializer):
        author_id = self.request.data.get('author_id')
        user = self.request.user
        instance = serializer.instance

        if author_id:
            try:
                author = User.objects.get(id=author_id)
            except User.DoesNotExist:
                return Response({"error": "Invalid author ID provided."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            author = instance.author  # Keep the current author if no new one is specified

        if author:
            serializer.save(author=author, author_id=author.id)
        else:
            return Response({"error": "You must provide a valid author ID to update the post."}, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        instance.delete()






# ----------------------------
