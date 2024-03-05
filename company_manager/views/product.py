from rest_framework import viewsets, permissions

from company_manager.models.category import Category
from ..serializers import  ProductSerializer

from company_manager.models import Product, Enterprise

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import HttpResponse
from ..models.product import Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    @action(detail=False, methods=['get'], url_path='search', url_name='search', permission_classes=[permissions.AllowAny])
    def search(self, request):
        data = request.query_params
        name = data.get('name')
        category = data.get('category')
        id = data.get('id')
        
        products = Product.objects.all()
        
        if name:
            products = products.filter(name__icontains=name)
        
        if category:
            # Obtener las categorías que coinciden con el nombre dado
            categories = Category.objects.filter(name__icontains=category)
            # Obtener los IDs de las categorías coincidentes
            category_ids = [cat.id for cat in categories]
            # Filtrar los productos por las categorías encontradas
            products = products.filter(categories__id__in=category_ids)

        
        if id:
            products = products.filter(id=id)
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='enterprise-products', url_name='enterprise-products', permission_classes=[permissions.AllowAny])
    def enterprise_products(self, request):
        enterprise_id = request.query_params.get('id')  # Obtener el id de la empresa de los parámetros de consulta
        try:
            enterprise = Enterprise.objects.get(id=enterprise_id)  # Obtener la empresa con el id dado
            products = enterprise.products.all()  # Obtener todos los productos asociados a la empresa
            serializer = ProductSerializer(products, many=True)  # Serializar los productos
            return Response(serializer.data, status=status.HTTP_200_OK)  # Devolver la lista de productos
        except Enterprise.DoesNotExist:
            return Response({'error': 'Enterprise not found'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['get'], url_path='generate-report', url_name='generate-report', permission_classes=[permissions.AllowAny])
    def generate_report(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="product_list.pdf"'

        products = Product.objects.all()

        # Crear un documento PDF
        pdf = SimpleDocTemplate(response, pagesize=letter)
    
        # Crear una lista para almacenar los datos de los productos
        product_data = []

        # Agregar encabezados a la lista de datos
        product_data.append(['ID', 'Name', 'Categories', 'Product Code','Enterprise Nit', 'Active', 'Created At'])

        # Agregar datos de productos a la lista de datos
        for product in products:
            # Obtener todas las categorías del producto como una cadena separada por comas
            categories = ', '.join(category.name for category in product.categories.all())
            product_data.append([product.id, product.name, categories, product.product_code,product.enterprise.nit , product.active, product.created_at])
        
        # Crear una tabla y definir el estilo de la tabla
        table = Table(product_data)
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

        table.setStyle(style)

        # Agregar la tabla al documento PDF
        pdf.build([table])

        return response
