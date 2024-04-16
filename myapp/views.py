
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class ClientViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Client.objects.all()
        serializer = ClientSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_id = request.data.get('created_by')  
        user = get_object_or_404(User, pk=user_id)

        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        queryset = Client.objects.all()
        client = get_object_or_404(queryset, pk=pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def patch(self, request, pk=None):
        client = self.get_object(pk)
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        client = self.get_object(pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def retrieve_with_projects(self, request, pk=None):
        client = get_object_or_404(Client, pk=pk)
        serializer = ClientSerializer(client)
        
        projects = client.project_set.all()
        projects_data = ProjectSerializer(projects, many=True).data

        client_data = serializer.data
        client_data['projects'] = projects_data

        return Response(client_data)
    
    def get_object(self, pk):
        return get_object_or_404(Client, pk=pk)
    
class ProjectViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Project.objects.all()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        project_data = request.data
        serializer = ProjectSerializer(data=project_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        queryset = Project.objects.all()
        client = get_object_or_404(queryset, pk=pk)
        serializer = ProjectSerializer(client)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        client = self.get_object(pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_object(self, pk):
        return get_object_or_404(Client, pk=pk)