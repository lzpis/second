class Product:
    def __init__(self, product_id, product_name):
        self.product_id = product_id
        self.product_name = product_name

    def __repr__(self):
        return f"Product(ID: {self.product_id}, Name: '{self.product_name}')"


class RecommendationSystem:
    def __init__(self):
        self.catalog = {}  # Store all products
        self.cart = []  # Current user's cart
        self.pairings = {}  # Track frequently bought together items

    def add_product_to_catalog(self, product):
        if product.product_id not in self.catalog:
            self.catalog[product.product_id] = product
            self.pairings[product.product_id] = {}

    def add_to_cart(self, product):
        if product.product_id in self.catalog and product not in self.cart:
            self.cart.append(product)
            # Update pairings count
            for other_product in self.cart:
                if other_product != product:
                    self.pairings[other_product.product_id].setdefault(product.product_id, 0)
                    self.pairings[other_product.product_id][product.product_id] += 1

    def recommend_products(self):
        recommendations = {}
        for product in self.cart:
            for paired_product_id, count in self.pairings[product.product_id].items():
                if paired_product_id not in [p.product_id for p in self.cart]:
                    recommendations.setdefault(paired_product_id, 0)
                    recommendations[paired_product_id] += count

        # Sorting recommendations by frequency and converting to product objects
        sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        return [self.catalog[prod_id] for prod_id, _ in sorted_recommendations]

# Example usage
rec_sys = RecommendationSystem()
rec_sys.add_product_to_catalog(Product(1, "Laptop"))
rec_sys.add_product_to_catalog(Product(2, "Mouse"))
rec_sys.add_product_to_catalog(Product(3, "Keyboard"))

## 继续使用之前定义的类

# 添加更多产品
rec_sys.add_product_to_catalog(Product(4, "Headphones"))
rec_sys.add_product_to_catalog(Product(5, "Monitor"))

# 模拟一些购物行为以形成“经常一起购买”的模式
rec_sys.add_to_cart(rec_sys.catalog[1])  # Laptop
rec_sys.add_to_cart(rec_sys.catalog[2])  # Mouse
rec_sys.add_to_cart(rec_sys.catalog[3])  # Keyboard

# 模拟另一个用户购买 Laptop 和 Headphones
rec_sys.add_to_cart(rec_sys.catalog[1])  # Laptop
rec_sys.add_to_cart(rec_sys.catalog[4])  # Headphones

# 模拟更多购物行为
rec_sys.add_to_cart(rec_sys.catalog[2])  # Mouse
rec_sys.add_to_cart(rec_sys.catalog[4])  # Headphones

# 模拟当前用户的购物车，包含 Laptop 和 Mouse
rec_sys.cart = [rec_sys.catalog[1], rec_sys.catalog[2]]

# 根据当前购物车中的商品，获取推荐商品
recommendations = rec_sys.recommend_products()
print(recommendations)

