from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .serializers import RegisterSerializer,AddTaskSerializer,UserDetailSerializer,TotalTaskSerializer
from rest_framework import generics,status
from django.shortcuts import get_object_or_404

from .models import AddTask
from accounts.models import UserModel

# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UpdateTaskView(APIView):
    permission_classes =[IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            try:
                task = AddTask.objects.get(pk=pk, user=request.user)
            except AddTask.DoesNotExist:
                return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = AddTaskSerializer(task)
            return Response(serializer.data,status=status.HTTP_200_OK)

        tasks = AddTask.objects.filter(user=request.user)
        serializer = AddTaskSerializer(tasks, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def patch(self, request, pk=None):
        try:
            task = AddTask.objects.get(pk=pk, user=request.user)
        except AddTask.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddTaskSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def delete(self, request, pk=None):
    #     try:
    #         task = AddTask.objects.get(pk=pk, user=request.user)
    #     except AddTask.DoesNotExist:
    #         return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    #     task.delete()
    #     return Response({"message": "Task deleted"}, status=status.HTTP_204_NO_CONTENT)
    

class AddTaskView(generics.ListCreateAPIView):
    
    serializer_class = AddTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AddTask.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskdeleteView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        task = get_object_or_404(AddTask, pk=pk)
        task.delete()
        return Response({"message": "Task deleted"}, status=status.HTTP_204_NO_CONTENT)
    

class UserDetailView(APIView):
    permission_classes =[IsAuthenticated]

    def get(self,request):
        user = request.user
        serializer = UserDetailSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class TotalTaskView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user = request.user

        total_tasks = AddTask.objects.filter(user=user).count()
        pending_tasks =AddTask.objects.filter(user=user,status="Todo").count()
        completed_tasks = AddTask.objects.filter(user=user,status="Done").count()
        progress_tasks = AddTask.objects.filter(user=user,status="In Progress").count()

        data ={
            "total_tasks":total_tasks,
            "pending_tasks":pending_tasks,
            "completed_tasks":completed_tasks,
            "progress_tasks":progress_tasks
        }
        serializer = TotalTaskSerializer(data)
        return Response(serializer.data,status=status.HTTP_200_OK)