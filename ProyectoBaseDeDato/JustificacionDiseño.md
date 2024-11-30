# Sistema de Ventas en Línea

## Dependencias funcionales (DFs):
1. `id_cliente -> nombre, email, direccion, telefono`
2. `id_producto -> nombre, descripcion, precio, stock, categoria`
3. `id_orden -> id_cliente, fecha`
4. `id_orden, id_producto -> cantidad`

## Claves candidatas:
- Tabla `Clientes`: **`id_cliente`**
- Tabla `Productos`: **`id_producto`**
- Tabla `Ordenes`: **`id_orden`**
- Tabla `Orden_Producto`: **`id_orden, id_producto`**

## Diseño normalizado (3FN):
El diseño normalizado divide la información en cuatro tablas para evitar redundancia y asegurar consistencia:

### Tabla: Clientes
- **Atributos:** `id_cliente (PK)`, `nombre`, `email`, `direccion`, `telefono`
- **Descripción:** Contiene información sobre los clientes que realizan compras en el sistema.

### Tabla: Productos
- **Atributos:** `id_producto (PK)`, `nombre`, `descripcion`, `precio`, `stock`, `categoria`
- **Descripción:** Almacena los productos disponibles para la venta.

### Tabla: Ordenes
- **Atributos:** `id_orden (PK)`, `id_cliente (FK)`, `fecha`
- **Descripción:** Registra las órdenes realizadas por los clientes, asociándolas a un cliente y una fecha específica.

### Tabla: Orden_Producto
- **Atributos:** `id_orden (FK)`, `id_producto (FK)`, `cantidad`
- **Descripción:** Asocia productos con órdenes, permitiendo múltiples productos por orden. La clave primaria es compuesta por `id_orden` y `id_producto`.

## Justificación del diseño:
1. **Evita redundancia:** Las tablas están diseñadas para almacenar datos únicos, evitando duplicación y garantizando consistencia.
2. **Flexibilidad:** Permite la gestión eficiente de clientes, productos y órdenes, con capacidad para escalar el diseño a funcionalidades adicionales.
3. **Cumple con la 3FN:** Cada atributo no clave depende únicamente de la clave primaria de su tabla, eliminando dependencias transitivas.
4. **Integridad referencial:** Las claves foráneas aseguran la consistencia de las relaciones entre tablas, como las asociaciones de productos a órdenes y de órdenes a clientes.