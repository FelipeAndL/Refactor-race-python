# legacy_checkout.py

ORDERS_PROCESSED = []


def _calculate_subtotal(items):
    subtotal = 0
    for item in items:
        if item["qty"] > 0:
            subtotal += item["price"] * item["qty"]
    return subtotal


def _calculate_customer_discount(customer_type, subtotal):
    if customer_type == "vip":
        return subtotal * (0.15 if subtotal >= 1000 else 0.10)
    if customer_type == "employee":
        return subtotal * 0.20
    if customer_type == "regular" and subtotal >= 800:
        return subtotal * 0.05
    return 0


def _calculate_coupon_discount(coupon, customer_type, subtotal):
    if coupon == "PROMO10":
        return subtotal * 0.10
    if coupon == "PROMO20" and subtotal >= 500:
        return subtotal * 0.20
    if coupon == "VIP50" and customer_type == "vip":
        return 50
    return 0


def _calculate_discount(customer_type, subtotal, coupon):
    discount = _calculate_customer_discount(customer_type, subtotal)
    discount += _calculate_coupon_discount(coupon, customer_type, subtotal)
    return min(discount, subtotal * 0.25)


def _calculate_weight(items):
    return sum(item.get("weight", 0) * item["qty"] for item in items)


def _calculate_shipping(subtotal, weight, state, express):
    if subtotal >= 500 and not express:
        return 0

    if state in {"MG", "SP", "RJ", "ES"}:
        shipping = 20 + weight * 0.4
    else:
        shipping = 35 + weight * 0.6

    return shipping * 1.8 if express else shipping


def _calculate_tax(discounted_total, state):
    tax_rates = {
        "MG": 0.07,
        "SP": 0.09,
        "RJ": 0.08,
        "ES": 0.07,
    }
    return discounted_total * tax_rates.get(state, 0.12)


def _calculate_points(customer_type, discounted_total, shipping, tax):
    divisor = 5 if customer_type == "vip" else 10
    return int((discounted_total + shipping + tax) / divisor)


def _find_duplicate_products(items):
    product_counts = {}
    for item in items:
        product_name = item["name"]
        product_counts[product_name] = product_counts.get(product_name, 0) + 1
    return [name for name, count in product_counts.items() if count > 1]


def _build_result(customer_name, subtotal, discount, shipping, tax, points,
                  duplicate_products):
    discounted_total = subtotal - discount
    total = round(discounted_total + shipping + tax, 2)

    result = {
        "customer": customer_name,
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "shipping": round(shipping, 2),
        "tax": round(tax, 2),
        "total": total,
        "points": points,
        "duplicate_products": duplicate_products,
    }
    return result


def _print_order_summary(customer_name, subtotal, discount, shipping, tax, total):
    print("Pedido processado para " + customer_name)
    print("Subtotal:", subtotal)
    print("Desconto:", discount)
    print("Frete:", shipping)
    print("Imposto:", tax)
    print("TOTAL:", total)


def process_order(customer, items, coupon="", state="MG", express=False):
    customer_name = customer["name"]
    customer_type = customer["type"]
    subtotal = _calculate_subtotal(items)
    discount = _calculate_discount(customer_type, subtotal, coupon)
    discounted_total = subtotal - discount
    shipping = _calculate_shipping(
        subtotal,
        _calculate_weight(items),
        state,
        express,
    )
    tax = _calculate_tax(discounted_total, state)
    points = _calculate_points(customer_type, discounted_total, shipping, tax)
    duplicate_products = _find_duplicate_products(items)
    result = _build_result(
        customer_name,
        subtotal,
        discount,
        shipping,
        tax,
        points,
        duplicate_products,
    )

    ORDERS_PROCESSED.append(result)

    _print_order_summary(
        customer_name,
        subtotal,
        discount,
        shipping,
        tax,
        result["total"],
    )

    return result
