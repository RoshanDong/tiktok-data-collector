"""
Order Aggregator Module for TikTok Shop Data Fetch Automation
Aggregates raw orders into daily sales metrics.
"""

from typing import List, Dict
from collections import defaultdict

from models import Order, DailySalesData, ProductSummary


class OrderAggregator:
    """Aggregates order data into daily sales summaries"""

    def __init__(self):
        """Initialize order aggregator"""
        pass

    def aggregate_orders(
        self,
        orders: List[Order],
        date_str: str
    ) -> DailySalesData:
        """
        Aggregate a list of orders into daily sales data.

        Args:
            orders: List of Order objects
            date_str: Date string in YYYY-MM-DD format

        Returns:
            DailySalesData object with aggregated metrics
        """
        # Calculate totals
        order_count = len(orders)
        total_revenue = sum(order.total_amount for order in orders)

        # Aggregate product sales
        product_sales = self._aggregate_products(orders)

        # Get top 10 products by quantity
        top_products = self._get_top_products(product_sales, limit=10)

        return DailySalesData(
            date=date_str,
            orderCount=order_count,
            totalRevenue=total_revenue,
            topProducts=top_products
        )

    def _aggregate_products(self, orders: List[Order]) -> Dict[str, Dict]:
        """
        Aggregate sales by product.

        Args:
            orders: List of Order objects

        Returns:
            Dict mapping product_id to aggregated sales data
        """
        product_data = defaultdict(lambda: {
            "productId": "",
            "productName": "",
            "quantitySold": 0,
            "revenue": 0.0
        })

        for order in orders:
            for item in order.items:
                product_id = item.product_id

                # Update product data
                product_data[product_id]["productId"] = product_id
                product_data[product_id]["productName"] = item.product_name
                product_data[product_id]["quantitySold"] += item.quantity
                product_data[product_id]["revenue"] += item.unit_price * item.quantity

        return product_data

    def _get_top_products(
        self,
        product_sales: Dict[str, Dict],
        limit: int = 10
    ) -> List[ProductSummary]:
        """
        Get top N products by quantity sold.

        Args:
            product_sales: Dict of aggregated product sales
            limit: Maximum number of products to return

        Returns:
            List of ProductSummary objects sorted by quantity descending
        """
        # Convert to ProductSummary objects
        products = [
            ProductSummary(
                productId=data["productId"],
                productName=data["productName"],
                quantitySold=data["quantitySold"],
                revenue=data["revenue"]
            )
            for data in product_sales.values()
            if data["productId"]  # Skip empty entries
        ]

        # Sort by quantity sold descending
        products.sort(key=lambda p: p.quantitySold, reverse=True)

        # Return top N
        return products[:limit]

    def calculate_daily_metrics(self, orders: List[Order]) -> Dict:
        """
        Calculate various daily metrics from orders.

        Args:
            orders: List of Order objects

        Returns:
            Dict with various metrics
        """
        if not orders:
            return {
                "orderCount": 0,
                "totalRevenue": 0.0,
                "averageOrderValue": 0.0,
                "totalItems": 0,
                "uniqueProducts": 0
            }

        total_revenue = sum(o.total_amount for o in orders)
        total_items = sum(sum(item.quantity for item in o.items) for o in orders)

        # Count unique products
        unique_products = set()
        for order in orders:
            for item in order.items:
                unique_products.add(item.product_id)

        return {
            "orderCount": len(orders),
            "totalRevenue": total_revenue,
            "averageOrderValue": total_revenue / len(orders) if orders else 0,
            "totalItems": total_items,
            "uniqueProducts": len(unique_products)
        }


def aggregate_from_api_response(
    orders_data: List[Dict],
    date_str: str
) -> DailySalesData:
    """
    Convenience function to aggregate orders directly from API response data.

    Args:
        orders_data: List of order dictionaries from API response
        date_str: Date string in YYYY-MM-DD format

    Returns:
        DailySalesData object
    """
    # Convert to Order objects
    orders = [Order.from_dict(o) for o in orders_data]

    # Aggregate
    aggregator = OrderAggregator()
    return aggregator.aggregate_orders(orders, date_str)


if __name__ == "__main__":
    # Test order aggregator
    from models import Order, OrderItem

    # Create test orders
    orders = [
        Order(
            order_id="O001",
            create_time=1717891200,
            total_amount=45.50,
            status="COMPLETED",
            items=[
                OrderItem("P001", "Brown Manga Lash", 2, 22.75),
                OrderItem("P002", "Natural Volume Lash", 1, 0.0)
            ]
        ),
        Order(
            order_id="O002",
            create_time=1717891201,
            total_amount=91.00,
            status="COMPLETED",
            items=[
                OrderItem("P001", "Brown Manga Lash", 4, 22.75)
            ]
        )
    ]

    # Aggregate
    aggregator = OrderAggregator()
    result = aggregator.aggregate_orders(orders, "2026-06-09")

    print("Daily Sales Data:")
    print(f"  Date: {result.date}")
    print(f"  Order Count: {result.orderCount}")
    print(f"  Total Revenue: ${result.totalRevenue:.2f}")
    print(f"  Top Products: {len(result.topProducts)}")

    for product in result.topProducts:
        print(f"    - {product.productName}: {product.quantitySold} sold, ${product.revenue:.2f}")

    # Test metrics
    metrics = aggregator.calculate_daily_metrics(orders)
    print(f"\nMetrics: {metrics}")