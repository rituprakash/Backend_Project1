#signup
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.forms import UserCreationForm
from rest_framework.permissions import AllowAny

#login
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.authtoken.models import Token

#add medicine
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from pharmacy.forms import MedicineForm

#list medicine
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from pharmacy.models import Medicine
from .serializers import MedicineSerializer
from rest_framework.permissions import AllowAny

#search medicine
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.filters import SearchFilter
from pharmacy.models import Medicine
from .serializers import MedicineSerializer


#edit medicine
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from pharmacy.forms import MedicineForm
from pharmacy.models import Medicine
from .serializers import MedicineSerializer

#delete medicine
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from pharmacy.models import Medicine
from rest_framework.permissions import AllowAny



#signup
@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    form = UserCreationForm(data=request.data)
    if form.is_valid():
        user = form.save()
        return Response("account created successfully", status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


#login
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)


#add medicine
@api_view(['POST'])
@permission_classes((AllowAny,))
def add_medicine(request):
    form = MedicineForm(request.POST)
    if form.is_valid():
        product = form.save()
        return Response({'id': product.id}, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


#list medicine
@api_view(['GET'])
@permission_classes((AllowAny,))
def medicines_list(request):
    products = Medicine.objects.all()
    serializer = MedicineSerializer(products, many=True)
    return Response(serializer.data)

#search medicine
class SearchAPIView(APIView):

    serializers_class =MedicineSerializer
    filter_backends =[SearchFilter]
    search_fields =['name']
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_queryset (self):
        q = self.request.query_params.get('search_query',None)
        if q:
            return Medicine.objects.filter(name__icontains=q)
        else:
            return Medicine.objects.none()
    
    def get(self,request):
        queryset = self.get_queryset()
        serializer = self.serializers_class(queryset, many=True)
        return Response(serializer.data)


#edit medicine
@api_view(['PUT'])
@permission_classes((AllowAny,))
def edit_medicine(request, pk):
    product = get_object_or_404(Medicine, pk=pk)
    form = MedicineForm(request.data, instance=product)
    if form.is_valid():
        form.save()
        serializer = MedicineSerializer(product)
        return Response(serializer.data)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    

#delete medicine
@api_view(['DELETE'])
@permission_classes((AllowAny,))
def delete_medicine(request, pk):
    try:
        product = Medicine.objects.get(pk=pk)
    except Medicine.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    product.delete()
    return Response("deleted successfully")