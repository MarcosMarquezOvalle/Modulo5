from __future__ import annotations

from datetime import datetime
from datetime import timezone
from typing import ClassVar, Optional

from pydantic import BaseModel, ConfigDict, Field


class OrderIn(BaseModel):
    """Input model for order data validation."""
    
    order_id: int | str = Field(..., description="Unique order identifier")
    customer_id: int | str = Field(..., description="Customer identifier")
    product_id: int | str = Field(..., description="Product identifier")
    quantity: int = Field(..., description="Quantity ordered", gt=0)
    price: float = Field(..., description="Price per unit", gt=0.0)
    tax_percentage: float = Field(default=16.0, description="Tax percentage", ge=0.0, le=100.0)
    
    DEFAULT_TAX_RATE: ClassVar[float] = 16.0

    @property
    def subtotal(self) -> float:
        """Calculate subtotal before tax."""
        return float(self.price * self.quantity)

    @property
    def total(self) -> float:
        """Calculate total including tax."""
        tax_amount: float = self.subtotal * (self.tax_percentage / 100)
        return round(self.subtotal + tax_amount, 2)

    def __eq__(self, other: object) -> bool:
        """Compare orders by ID."""
        if not isinstance(other, OrderIn):
            return NotImplemented
        return self.order_id == other.order_id

    def __lt__(self, other: OrderIn) -> bool:
        """Compare orders by total amount."""
        if not isinstance(other, OrderIn):
            return NotImplemented
        return self.total < other.total

    def __le__(self, other: OrderIn) -> bool:
        """Check if order total is less than or equal to another."""
        if not isinstance(other, OrderIn):
            return NotImplemented
        return self.total <= other.total


class OrderOut(BaseModel):
    """Output model for order data with metadata."""
    
    model_config = ConfigDict(from_attributes=True)
    
    order_id: int | str = Field(..., description="Unique order identifier")
    customer_id: int | str = Field(..., description="Customer identifier")
    product_id: int | str = Field(..., description="Product identifier")
    quantity: int = Field(..., description="Quantity ordered", gt=0)
    price: float = Field(..., description="Price per unit", gt=0.0)
    tax_percentage: float = Field(default=16.0, description="Tax percentage", ge=0.0, le=100.0)
    created_at: datetime = Field(..., description="Order creation timestamp")
    
    DEFAULT_TAX_RATE: ClassVar[float] = 16.0

    @property
    def subtotal(self) -> float:
        """Calculate subtotal before tax."""
        return float(self.price * self.quantity)

    @property
    def total(self) -> float:
        """Calculate total including tax."""
        tax_amount: float = self.subtotal * (self.tax_percentage / 100)
        return round(self.subtotal + tax_amount, 2)

    def __eq__(self, other: object) -> bool:
        """Compare orders by ID."""
        if not isinstance(other, OrderOut):
            return NotImplemented
        return self.order_id == other.order_id

    def __lt__(self, other: OrderOut) -> bool:
        """Compare orders by total amount."""
        if not isinstance(other, OrderOut):
            return NotImplemented
        return self.total < other.total

    def __le__(self, other: OrderOut) -> bool:
        """Check if order total is less than or equal to another."""
        if not isinstance(other, OrderOut):
            return NotImplemented
        return self.total <= other.total


class OrderEntity:
    """Domain entity for order data representation."""
    
    def __init__(
        self,
        order_id: Optional[int | str] = None,
        customer_id: Optional[int | str] = None,
        product_id: Optional[int | str] = None,
        quantity: Optional[int] = None,
        price: Optional[float] = None,
        tax_percentage: Optional[float] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        """Initialize order entity with provided parameters.
        
        Args:
            order_id: Unique order identifier
            customer_id: Customer identifier
            product_id: Product identifier
            quantity: Quantity ordered
            price: Price per unit
            tax_percentage: Tax percentage (default: 16.0)
            created_at: Order creation timestamp (default: current UTC time)
        """
        self.order_id: Optional[int | str] = order_id
        self.customer_id: Optional[int | str] = customer_id
        self.product_id: Optional[int | str] = product_id
        self.quantity: Optional[int] = quantity
        self.price: Optional[float] = price
        self.tax_percentage: Optional[float] = tax_percentage
        self.created_at: datetime = created_at or datetime.now(timezone.utc)




# --- EXAMPLE INSTANCES ---

order_entrada_1: OrderIn = OrderIn(
    order_id="4", customer_id="4", product_id="4",
    quantity=1, price=1000.0, tax_percentage=16.0,
)
order_entrada_2: OrderIn = OrderIn(
    order_id=2, customer_id=2,
    product_id=2, quantity=1, price=600.0, tax_percentage=16.0,
)
order_entrada_3: OrderIn = OrderIn(
    order_id=3, customer_id=3,
    product_id=3, quantity=1, price=300.0, tax_percentage=16.0,
)

# --- PROCESS: CONVERSION FROM MODEL TO ENTITY ---

nueva_entidad: OrderEntity = OrderEntity(**order_entrada_2.model_dump())

nueva_entidad.order_id = 1

# --- PROCESS: CONVERT ENTITY BACK TO OUTPUT MODEL ---

respuesta_cliente: OrderOut = OrderOut.model_validate(nueva_entidad)

print(respuesta_cliente.model_dump_json())
