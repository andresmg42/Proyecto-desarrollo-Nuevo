from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from pedidos.models import Pedido, PedidoProducto
from productos.models import Producto, Categoria
from django.contrib.auth.models import User
from datetime import datetime, time
from django.contrib.auth.hashers import make_password

class PedidoViewSetTest(APITestCase):
    def setUp(self):
        test_password = make_password('testpass123!')
        self.user = User.objects.create_user(username='cliente', password=test_password)
        self.client.force_authenticate(user=self.user)

        self.pedido = Pedido.objects.create(
            usuarios=self.user,
            metodo_pago='Efectivo',
            direccion='Av. Central',
            hora=time(10, 0, 0),
            estado_pedido=False,
            fecha=datetime.today().date()
        )

    def test_list_pedidos(self):
        url = reverse('pedidos-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_pedido(self):
        url = reverse('pedidos-detail', kwargs={'pk': self.pedido.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.pedido.id)

    def tearDown(self):
        User.objects.all().delete()
        Pedido.objects.all().delete()
        Producto.objects.all().delete()
        Categoria.objects.all().delete()

class PedidoProductoViewSetTest(APITestCase):
    def setUp(self):
        test_password = make_password('testpass123!')
        self.user = User.objects.create_user(username='cliente', password=test_password)
        self.client.force_authenticate(user=self.user)


        self.categoria = Categoria()
        self.categoria.save()
        

        self.producto = Producto.objects.create(
            categoria=self.categoria,
            estado_producto=True,
            nombre='Hamburguesa',
            precio=25.0,
            descripcion='Hamburguesa doble carne',
            cantidad_producto=20
        )


        self.pedido = Pedido.objects.create(
            usuarios=self.user,
            metodo_pago='Tarjeta',
            direccion='Calle Luna',
            hora=time(13, 0, 0),
            estado_pedido=True,
            fecha=datetime.today().date()
        )

        self.pedido_producto = PedidoProducto.objects.create(
            pedido_ppid=self.pedido,
            producto_ppid=self.producto,
            cantidad_producto_carrito=2
        )

    def test_list_pedido_productos(self):
        url = reverse('pedidos_productos-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_pedido_producto(self):
        url = reverse('pedidos_productos-detail', kwargs={'pk': self.pedido_producto.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.pedido_producto.id)
    def tearDown(self):
        User.objects.all().delete()
        Pedido.objects.all().delete()
        Producto.objects.all().delete()
        Categoria.objects.all().delete()