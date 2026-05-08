from google.adk.tools import FunctionTool

def get_product_recommendation(query: str) -> str:
    product_catalog = {
        "laptop": [
            "ASUS VivoBook 15 - Rp 7.500.000 (Ryzen 5, 8GB RAM)",
            "Lenovo IdeaPad Slim 3 - Rp 6.800.000 (Intel i5, 8GB RAM)",
            "Acer Aspire 5 - Rp 8.200.000 (Intel i5, 16GB RAM)"
        ],
        "hp": [
            "Samsung Galaxy A55 - Rp 4.500.000",
            "Xiaomi Redmi Note 13 - Rp 2.800.000",
            "iPhone 15 - Rp 14.000.000"
        ],
        "headphone": [
            "Sony WH-1000XM5 - Rp 4.200.000 (Noise Cancelling)",
            "JBL Tune 770NC - Rp 1.500.000",
            "Anker Soundcore Q45 - Rp 700.000"
        ]
    }

    query_lower = query.lower()
    recommendations = []

    for keyword, products in product_catalog.items():
        if keyword in query_lower:
            recommendations.extend(products)

    if recommendations:
        product_list = "\n".join([f"• {p}" for p in recommendations])
        return f"Berikut rekomendasi produk untuk '{query}':\n\n{product_list}"

    return (
        f"Maaf, saya tidak menemukan produk spesifik untuk '{query}'. "
        "Coba cari dengan kata kunci seperti: laptop, hp, headphone, dll."
    )


product_tool = FunctionTool(func=get_product_recommendation)