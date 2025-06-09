import { Card, CardContent } from "./ui/card"

const ProductCard = ({ product }) => {
    return (
        <Card className="rounded-xl shadow-sm">
            <CardContent className="p-4 space-y-2">
                <h3 className="font-semibold text-lg">{product.product_title}</h3>
                <p><strong>Price:</strong> {product.price}</p>
                <p><strong>MOQ:</strong> {product.moq || "N/A"}</p>
                <p><strong>Supplier:</strong> {product.supplier_name}</p>
                <p><strong>Rating:</strong> {product.rating}</p>
                <a href={product.product_url} target="_blank" rel="noreferrer" className="text-blue-600 underline">
                    View Product
                </a>
            </CardContent>
        </Card>
    )
}

export default ProductCard