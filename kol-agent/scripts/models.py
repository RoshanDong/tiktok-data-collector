"""
Data Models for TikTok Shop Data Fetch Automation
Based on data-model.md specification
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List
from enum import Enum
import json


class FetchStatus(Enum):
    """Status of a fetch operation"""
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"


@dataclass
class ProductSummary:
    """Summary of a product's sales performance"""
    productId: str
    productName: str
    quantitySold: int
    revenue: float

    def to_dict(self) -> dict:
        return {
            "productId": self.productId,
            "productName": self.productName,
            "quantitySold": self.quantitySold,
            "revenue": round(self.revenue, 2)
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ProductSummary':
        return cls(
            productId=data.get('productId', ''),
            productName=data.get('productName', ''),
            quantitySold=int(data.get('quantitySold', 0)),
            revenue=float(data.get('revenue', 0.0))
        )


@dataclass
class DailySalesData:
    """
    Represents one day's sales summary from TikTok Shop.
    Corresponds to data-model.md entity.
    """
    date: str  # YYYY-MM-DD format
    orderCount: int
    totalRevenue: float
    topProducts: List[ProductSummary] = field(default_factory=list)

    def __post_init__(self):
        """Validate and normalize data after initialization"""
        # Ensure orderCount is non-negative
        if self.orderCount < 0:
            raise ValueError("orderCount must be >= 0")

        # Ensure totalRevenue has max 2 decimal places
        self.totalRevenue = round(self.totalRevenue, 2)

        # Ensure topProducts has max 10 items
        if len(self.topProducts) > 10:
            self.topProducts = self.topProducts[:10]

    def to_dict(self) -> dict:
        return {
            "date": self.date,
            "orderCount": self.orderCount,
            "totalRevenue": self.totalRevenue,
            "topProducts": [p.to_dict() for p in self.topProducts]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'DailySalesData':
        products = [
            ProductSummary.from_dict(p)
            for p in data.get('topProducts', [])
        ]
        return cls(
            date=data['date'],
            orderCount=int(data['orderCount']),
            totalRevenue=float(data['totalRevenue']),
            topProducts=products
        )

    def to_excel_row(self) -> dict:
        """Convert to Excel row format with JSON string for topProducts"""
        return {
            "Date": self.date,
            "Order Count": self.orderCount,
            "Total Revenue": self.totalRevenue,
            "Top Products": json.dumps([p.to_dict() for p in self.topProducts], ensure_ascii=False)
        }


@dataclass
class FetchLog:
    """
    Audit trail of all fetch operations.
    Corresponds to data-model.md entity.
    """
    timestamp: str  # ISO 8601 format
    status: FetchStatus
    dateQueried: str  # YYYY-MM-DD
    orderCount: int
    totalRevenue: float
    errorMessage: Optional[str] = None
    retryCount: int = 0

    def to_dict(self) -> dict:
        result = {
            "timestamp": self.timestamp,
            "status": self.status.value,
            "dateQueried": self.dateQueried,
            "orderCount": self.orderCount,
            "totalRevenue": round(self.totalRevenue, 2),
            "retryCount": self.retryCount
        }
        if self.errorMessage:
            result["errorMessage"] = self.errorMessage
        return result

    @classmethod
    def from_dict(cls, data: dict) -> 'FetchLog':
        status = FetchStatus(data.get('status', 'failure'))
        return cls(
            timestamp=data['timestamp'],
            status=status,
            dateQueried=data['dateQueried'],
            orderCount=int(data['orderCount']),
            totalRevenue=float(data['totalRevenue']),
            errorMessage=data.get('errorMessage'),
            retryCount=int(data.get('retryCount', 0))
        )

    def to_jsonl_line(self) -> str:
        """Convert to JSONL line format"""
        return json.dumps(self.to_dict(), ensure_ascii=False)


@dataclass
class OrderItem:
    """Individual item in an order"""
    product_id: str
    product_name: str
    quantity: int
    unit_price: float

    @classmethod
    def from_dict(cls, data: dict) -> 'OrderItem':
        return cls(
            product_id=data.get('product_id', ''),
            product_name=data.get('product_name', ''),
            quantity=int(data.get('quantity', 0)),
            unit_price=float(data.get('unit_price', 0.0))
        )


@dataclass
class Order:
    """Represents a single order from TikTok API"""
    order_id: str
    create_time: int
    total_amount: float
    status: str
    items: List[OrderItem] = field(default_factory=list)

    @property
    def revenue(self) -> float:
        return self.total_amount

    @classmethod
    def from_dict(cls, data: dict) -> 'Order':
        items = [
            OrderItem.from_dict(item)
            for item in data.get('items', [])
        ]
        return cls(
            order_id=data.get('order_id', ''),
            create_time=int(data.get('create_time', 0)),
            total_amount=float(data.get('total_amount', 0.0)),
            status=data.get('status', ''),
            items=items
        )


if __name__ == "__main__":
    # Test models
    sales_data = DailySalesData(
        date="2026-06-09",
        orderCount=156,
        totalRevenue=4523.50,
        topProducts=[
            ProductSummary("P001", "Brown Manga Lash", 50, 1250.00),
            ProductSummary("P002", "Natural Volume Lash", 35, 875.00)
        ]
    )
    print("DailySalesData test:")
    print(json.dumps(sales_data.to_dict(), indent=2, ensure_ascii=False))

    log = FetchLog(
        timestamp="2026-06-10T06:00:15Z",
        status=FetchStatus.SUCCESS,
        dateQueried="2026-06-09",
        orderCount=156,
        totalRevenue=4523.50,
        retryCount=0
    )
    print("\nFetchLog test:")
    print(log.to_jsonl_line())