import { useEffect, useState } from "react"
import SearchManager from "../components/search_manager"
import ProductCard from "../components/product_card"
import { useEmail } from "../hooks/use-email"
import { useSearchParams } from "react-router-dom"

const Dashboard = () => {
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const { email } = useEmail()

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

  const [searchParams] = useSearchParams()
  const prefillKeyword = searchParams.get("keyword") || ""

  const [keyword, setKeyword] = useState("")

  useEffect(() => {
    if (prefillKeyword) setKeyword(prefillKeyword)
  }, [prefillKeyword])

  const handleSearch = async ({ keyword, maxCount }) => {
    setLoading(true)
    try {
      console.log("Sending request:", { keyword, maxCount });

      const res = await fetch(`${API_BASE_URL}/search-and-notify`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
        keyword,
        max_results: parseInt(maxCount) || 5,
        receiver: email 
        }),
      });

      const data = await res.json()

      if (!res.ok) {
        console.error("[Frontend Error]", data) 
        return
      }

      setResults(data.products || [])
    } catch (err) {
      console.error("Search failed:", err)
    } finally {
      setLoading(false)
  }
}

  return (
    <div className="min-h-screen w-full px-4 py-12">
      <div className="max-w-6xl mx-auto space-y-8">
        <h1 className="text-4xl sm:text-5xl font-bold tracking-tight text-center">
          Alibaba Product Monitoring Agent
        </h1>

        <SearchManager onSearch={handleSearch} loading={loading} keyword={keyword} setKeyword={setKeyword} />

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
          {results.map((product, idx) => (
            <ProductCard key={idx} product={product} />
          ))}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
