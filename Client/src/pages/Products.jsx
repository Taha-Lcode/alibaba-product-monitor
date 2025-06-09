import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { Button } from "../components/ui/button"

const UNSPLASH_KEY = import.meta.env.VITE_UNSPLASH_ACCESS_KEY
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const fetchImageForKeyword = async (keyword) => {
  const cached = localStorage.getItem(`image:${keyword}`)
  if (cached) return cached

  const url = `https://api.unsplash.com/search/photos?query=${encodeURIComponent(keyword)}&client_id=${UNSPLASH_KEY}&per_page=1`
  try {
    const res = await fetch(url)
    const data = await res.json()
    const img = data?.results?.[0]?.urls?.regular || null
    if (img) localStorage.setItem(`image:${keyword}`, img)
    return img
  } catch (err) {
    console.error("Failed to fetch image:", err)
    return null
  }
}

const Products = () => {
  const [keywords, setKeywords] = useState([])
  const [images, setImages] = useState({})
  const navigate = useNavigate()

  useEffect(() => {
    fetch(`${API_BASE_URL}/keywords`)
      .then((res) => res.json())
      .then(async (data) => {
        const keys = data.keywords || []
        setKeywords(keys)

        const imgMap = {}
        for (const keyword of keys) {
          const url = await fetchImageForKeyword(keyword)
          if (url) imgMap[keyword] = url
        }
        setImages(imgMap)
      })
      .catch((err) => console.error("Failed to fetch keywords", err))
  }, [])

  const handleReSearch = (keyword) => {
    navigate(`/?keyword=${encodeURIComponent(keyword)}`)
  }

  return (
    <div className="min-h-screen w-full px-4 py-12">
      <div className="max-w-6xl mx-auto space-y-8">
        <h1 className="text-3xl font-bold mb-6">🔎 Previously Searched Products</h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {keywords.map((keyword) => (
            <div
              key={keyword}
              className="group relative rounded-xl overflow-hidden shadow-md border bg-cover bg-center h-52"
              style={{ backgroundImage: `url(${images[keyword] || "/fallback.jpg"})` }}
            >
              <div className="absolute inset-0 bg-black/30 group-hover:bg-black/60 transition duration-300 flex items-center justify-center opacity-0 group-hover:opacity-100">
                <Button
                  className="bg-white text-black hover:bg-gray-200 cursor-pointer"
                  onClick={() => handleReSearch(keyword)}
                >
                  Re-Search
                </Button>
              </div>
              <div className="absolute bottom-0 left-0 right-0 bg-black/60 text-white text-center py-2 px-3 text-sm font-semibold">
                {keyword}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Products
