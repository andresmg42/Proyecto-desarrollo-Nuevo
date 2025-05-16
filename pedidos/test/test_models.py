from django.test import TestCase
from pedidos.models import Pedido, PedidoProducto
from productos.models import Producto, Categoria
from django.contrib.auth.models import User
from datetime import datetime, time

class PedidoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cliente', password='1234')
        self.pedido = Pedido.objects.create(
            usuarios=self.user,
            metodo_pago='Tarjeta',
            direccion='Calle Real',
            hora=time(11, 0, 0),
            estado_pedido=True,
            fecha=datetime.today().date()
        )

    def test_pedido_str(self):
        self.assertIn(str(self.pedido.id), str(self.pedido))

    def test_pedido_fields(self):
        self.assertEqual(self.pedido.metodo_pago, 'Tarjeta')
        self.assertEqual(self.pedido.direccion, 'Calle Real')
        self.assertTrue(self.pedido.estado_pedido)

    def tearDown(self):
        User.objects.all().delete()
        Pedido.objects.all().delete()
        Producto.objects.all().delete()
        Categoria.objects.all().delete()

class PedidoProductoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cliente', password='1234')
        

        self.categoria = Categoria()
        self.categoria.save()
        

        self.producto = Producto.objects.create(
            categoria=self.categoria,
            estado_producto=True,
            nombre='Refresco',
            precio=5.0,
            descripcion='Bebida refrescante',
            cantidad_producto=10
        )
        
        self.pedido = Pedido.objects.create(
            usuarios=self.user,
            metodo_pago='Efectivo',
            direccion='Av. Sol',
            hora=time(15, 0, 0),
            estado_pedido=False,
            fecha=datetime.today().date()
        )
        self.pedido_producto = PedidoProducto.objects.create(
            pedido_ppid=self.pedido,
            producto_ppid=self.producto,
            cantidad_producto_carrito=1
        )

    def test_pedido_producto_str(self):
        self.assertEqual(str(self.pedido_producto), f'PedidoProducto object ({self.pedido_producto.id})')

    def test_pedido_producto_fields(self):
        self.assertEqual(self.pedido_producto.cantidad_producto_carrito, 1)
        self.assertEqual(self.pedido_producto.pedido_ppid, self.pedido)
        self.assertEqual(self.pedido_producto.producto_ppid, self.producto)
    def tearDown(self):
        User.objects.all().delete()
        Pedido.objects.all().delete()
        Producto.objects.all().delete()
        Categoria.objects.all().delete()