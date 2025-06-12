import { Card, CardContent } from "./ui/card"

const ProductCard = ({ product }) => {
    return (
        <Card className="rounded-xl shadow-md overflow-hidden w-full">
            {product.image ? (
                <img
                    src={product.image.startsWith("//") ? `https:${product.image}` : product.image}
                    alt={product.product_title}
                    className="w-full h-48 object-cover"
                />
            ) : (
                <div className="w-full h-48 bg-gray-200 flex items-center justify-center text-gray-500">
                    No Image
                </div>
            )}

            <CardContent className="p-4 space-y-2">
                <h3 className="font-semibold text-lg line-clamp-2">{product.product_title}</h3>

                <p><strong>Price:</strong> {product.price || "N/A"}</p>
                <p><strong>MOQ:</strong> {product.moq || "N/A"}</p>
                <p><strong>Supplier:</strong> {product.supplier_name !== "Unknown" ? product.supplier_name : "Not Provided"}</p>

                <a
                    href={product.product_url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-blue-600 underline inline-block mt-2"
                >
                    View Product
                </a>
            </CardContent>
        </Card>
    )
}

export default ProductCard