from rest_framework import viewsets, permissions
from ..serializers import OrderSerializer

from company_manager.models import Product, Order

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import HttpResponse
from ..models.product import Product

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    @action(detail=False, methods=['post'], url_path='create-order', url_name='create-order', permission_classes=[permissions.AllowAny])
    def create_order(self, request):
        data = request.data
        product_ids = data.get('products')
        payment_currency = data.get('payment_currency')
    
        total = 0  # Inicializar el total
    
        # Calcular el total de la orden
        for product_id in product_ids:
            try:
                product = Product.objects.get(id=product_id)
                # Obtener el valor del producto en la moneda de pago
                currency_info = next((currency for currency in product.currencies if currency['code'].lower() == payment_currency.lower()), None)
                if currency_info:
                    total += currency_info['value']
                else:
                    return Response({'error': f'Currency {payment_currency} not supported for product {product_id}'}, status=status.HTTP_400_BAD_REQUEST)
            except Product.DoesNotExist:
                return Response({'error': f'Product with id {product_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    
        # Crear una instancia de la orden y asignar el total
        order = Order.objects.create(payment_currency=payment_currency, total=total)
    
        # Agregar los productos a la orden
        for product_id in product_ids:
            product = Product.objects.get(id=product_id)
            order.products.add(product)
    
        return Response({'message': 'Order created successfully', 'total': total}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='print-order', url_name='print-order', permission_classes=[permissions.AllowAny])
    def print_order(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="order_details.pdf"'
        
        params = request.query_params
        order_id = params.get('id')
        
        try:
            order = Order.objects.get(id=order_id)
            
            # Obtener los productos de la orden
            products = order.products.all()
            
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
        except Order.DoesNotExist:
            return Response({'error': f'Order with id {order_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
        