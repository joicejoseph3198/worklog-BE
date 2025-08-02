from http import HTTPStatus
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TaskCreateSerializer, TaskResponseSerializer, TaskUpdateSerializer, NotesSerializer
from .models import Task, Notes, Schedule
from .utils import JWTAuthentication
import datetime

class TaskCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        user_id = request.auth["sub"]
        request.data["user_id"] = user_id
        serializer = TaskCreateSerializer(data = request.data)
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
        return Response({'data': serializer.data, 'message': 'Task fetched successfully'}, HTTPStatus.OK)

class TaskGetByDateView(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        date = request.GET.get("date")
        user_id = request.auth["sub"]
        try:
            tasks = Task.objects.filter(date=date,user_id=user_id)
            serializer = TaskResponseSerializer(tasks, many=True)
        except Task.DoesNotExist:
            return Response({"message": "Task not found"}, status=HTTPStatus.NOT_FOUND)
        return Response({'data': serializer.data, 'message': 'Task fetched successfully'}, HTTPStatus.OK)

class TaskUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    def patch(self, request):
        user_id = request.auth["sub"]
        task_id = request.data.get("id")
        if not task_id:
            return Response({"message": "Task ID is required"}, status=HTTPStatus.BAD_REQUEST)
        try:
            task = Task.objects.get(id=task_id, user_id=user_id)
        except Task.DoesNotExist:
            return Response({"message": "Task not found"}, status=HTTPStatus.NOT_FOUND)
        # Use partial=True so only provided fields are updated
        serializer = TaskUpdateSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.OK)
        else:
            return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


class TaskDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    def delete(self, request,id):
        user_id = request.auth["sub"]
        try:
            task = Task.objects.get(id=id, user_id = user_id)
        except Task.DoesNotExist:
            return Response({"message": "Task not found"}, status=HTTPStatus.NOT_FOUND)
        task.delete()
        return Response({"message": "Task deleted successfully"}, status=HTTPStatus.NO_CONTENT)


class TaskCopyFromDateView(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        user_id = request.auth["sub"]
        source_date = request.data.get("source_date")
        target_date = request.data.get("target_date")
        
        if not source_date or not target_date:
            return Response({"message": "Both source_date and target_date are required"}, status=HTTPStatus.BAD_REQUEST)
        
        try:
            # Get all tasks from source date
            source_tasks = Task.objects.filter(date=source_date, user_id=user_id)
            
            if not source_tasks.exists():
                return Response({"message": "No tasks found for the source date"}, status=HTTPStatus.NOT_FOUND)
            
            # Copy tasks to target date
            copied_tasks = []
            for source_task in source_tasks:
                # Create new task with same data but new date
                new_task = Task.objects.create(
                    user_id=user_id,
                    title=source_task.title,
                    tag=source_task.tag,
                    description=source_task.description,
                    date=target_date,
                    status='not-started',  # Reset status for copied tasks
                    ticked=False  # Reset completion status
                )
                copied_tasks.append(new_task)
            
            # Serialize the copied tasks
            serializer = TaskResponseSerializer(copied_tasks, many=True)
            return Response({
                'data': serializer.data, 
                'message': f'Successfully copied {len(copied_tasks)} tasks from {source_date} to {target_date}'
            }, status=HTTPStatus.CREATED)
            
        except Exception as e:
            return Response({"message": f"Error copying tasks: {str(e)}"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)


class NotesGetByDateView(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        user_id = request.auth["sub"]
        date_str = request.GET.get("date")
        try:
            # Use filter().first() to handle potential duplicates gracefully
            note = Notes.objects.filter(date=date_str, user_id=user_id).first()
            if note:
                serializer = NotesSerializer(note)
                return Response(serializer.data, HTTPStatus.OK)
            else:
                return Response({"message": "Note not found"}, status=HTTPStatus.NOT_FOUND)
        except Exception as e:
            return Response({"message": "Error fetching note"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)


class NoteUpsertDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        user_id = request.auth["sub"]
        body = request.data.get("body")
        date_str = request.data.get("date")

        if not user_id:
            return Response({"error": "user_id is required."}, status=HTTPStatus.BAD_REQUEST)

        if not date_str:
            return Response({"error": "date is required."}, status=HTTPStatus.BAD_REQUEST)

        # Handle potential duplicates by using update_or_create instead of get_or_create
        note, created = Notes.objects.update_or_create(
            user_id=user_id, 
            date=date_str,
            defaults={'body': body if body and body.strip() else ''}
        )

        # Always return the note data, regardless of content
        serializer = NotesSerializer(note)
        return Response(serializer.data, status=HTTPStatus.OK)

class ScheduleUpsertDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        user_id = request.auth["sub"]
        date = request.data.get("date")
        schedule_list = request.data.get("schedule", [])

        if not date or not isinstance(schedule_list, list):
            return Response({"error": "Invalid payload"}, status=HTTPStatus.BAD_REQUEST)

        results = []
        for item in schedule_list:
            hour = item.get("hour")
            entry = item.get("entry", "").strip()

            if hour is None:
                continue  # skip invalid items

            # DELETE if entry is empty
            if entry == "":
                Schedule.objects.filter(user_id=user_id, date=date, hour=hour).delete()
                results.append({"hour": hour, "action": "deleted"})
            else:

                # UPSERT (update if exists, else create)
                obj, created = Schedule.objects.update_or_create(
                    user_id=user_id,
                    date=date,
                    hour=hour,
                    defaults={"detail": entry}
                )
                results.append({"hour": hour, "action": "created" if created else "updated"})

        return Response({"result": results}, status=HTTPStatus.OK)

class ScheduleFetchView(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        user_id = request.auth["sub"]
        date = request.GET.get("date")

        if not date:
            return Response({"error": "Missing 'date' query parameter"}, status=HTTPStatus.BAD_REQUEST)

        entries = Schedule.objects.filter(user_id=user_id, date=date).values("hour", "detail").order_by("hour")

        return Response({"data": list(entries)}, status=HTTPStatus.OK)
