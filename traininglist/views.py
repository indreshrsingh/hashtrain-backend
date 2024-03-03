from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Training
from .serializers import TrainingSerializer
from .permissions import IsAdminOrReadOnly



@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly])
def training_list(request):
    """
    List all trainings or create a new training
    """
    if request.method == 'GET':
        trainings = Training.objects.all()
        serializer = TrainingSerializer(trainings, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Pre-fill JSON data with empty values for admin users
        if request.user and request.user.is_staff:
            data = {'title': '', 'description': '', 'fees': None, 'duration': ''}
        else:
            data = request.data
        serializer = TrainingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrReadOnly])
def training_detail(request, pk):
    """
    Retrieve, update or delete a training instance
    """
    try:
        training = Training.objects.get(pk=pk)
    except Training.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TrainingSerializer(training)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # If the request is from an admin user, pre-fill the JSON data with empty values
        if request.user and request.user.is_staff:
            data = {'title': '', 'description': '', 'price': None, 'duration': ''}
            partial = True  # Allow partial updates
        else:
            data = request.data
            partial = False  # Do not allow partial updates
        
        serializer = TrainingSerializer(training, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        training.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


