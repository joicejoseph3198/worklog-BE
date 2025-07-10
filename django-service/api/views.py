from http import HTTPStatus
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TaskCreateSerializer, TaskResponseSerializer
from .models import Task
from .utils import JWTAuthentication

class TaskCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        user_id = request.auth["sub"]
        data = {
            'user_id': user_id,
            'tag': request.data.get('tag'),
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'date': request.data.get('date')
        }
        serializer = TaskCreateSerializer(data = data)
        if serializer.is_valid():
            saved_task = serializer.save()
            response_serializer = TaskResponseSerializer(saved_task)
            return Response({'data' : response_serializer.data, 'message': "Task added successfully"}, status=HTTPStatus.CREATED)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)

class TaskGetByIdView(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self, request, id):
        user_id = request.auth["sub"]
        try:
            task = Task.objects.get(user_id=user_id, id=id)
        except Task.DoesNotExist:
            return Response({"message": "Task not found"}, status=HTTPStatus.NOT_FOUND)
        serializer = TaskResponseSerializer(task)
        return Response({'date': serializer.data, 'message': 'Task fetched successfully'}, HTTPStatus.OK)

class TaskGetByDate(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        date = request.GET.get("date")
        user_id = request.auth["sub"]
        try:
            tasks = Task.objects.filter(date=date,user_id=user_id)
            serializer = TaskResponseSerializer(tasks, many=True)
        except Task.DoesNotExist:
            return Response({"message": "Task not found"}, status=HTTPStatus.NOT_FOUND)
        return Response({'date': serializer.data, 'message': 'Task fetched successfully'}, HTTPStatus.OK)
