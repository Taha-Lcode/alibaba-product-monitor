import { useState, useEffect } from "react"
import { Input } from "./ui/input"
import { Label } from "./ui/label"
import { Card, CardContent } from "./ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select"
import { Button } from "./ui/button"
import { toast } from "sonner"
import { useEmail } from "../hooks/use-email"
import debounce from "lodash.debounce"

const SearchManager = ({ onSearch, loading }) => {
  const [keyword, setKeyword] = useState("")
  const [allCategories, setAllCategories] = useState([])
  const [suggestions, setSuggestions] = useState([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [maxCount, setMaxCount] = useState("5")
  const { email } = useEmail()

  useEffect(() => {
    const fetchAllCategories = async () => {
      try {
        const res = await fetch("http://localhost:5000/categories")
        const data = await res.json()
        setAllCategories(data)
        setSuggestions(data)
      } catch (err) {
        console.error("Failed to load categories:", err)
      }
    }

    fetchAllCategories()
  }, [])

  useEffect(() => {
    const fetchSuggestions = async () => {
      if (!keyword.trim()) return setSuggestions([])
      try {
        const res = await axios.get(`http://localhost:5000/categories?q=${keyword}`)
        setSuggestions(res.data)
      } catch (err) {
        console.error("Error fetching suggestions", err)
      }
    }

    const debounce = setTimeout(fetchSuggestions, 300)
    return () => clearTimeout(debounce)
  }, [keyword])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!keyword.trim()) return toast.error("Please enter a product keyword.")
    onSearch({ keyword, maxCount, email })
    setSuggestions([])
  }

  const handleSuggestionClick = (val) => {
    setKeyword(val)
    setSuggestions([])
  }

  const fetchSuggestions = debounce(async (query) => {
    if (!query.trim()) {
      setSuggestions([])
      return
    }

    try {
      const res = await fetch(`http://localhost:5000/categories?q=${query}`)
      const data = await res.json()
      setSuggestions(data)
      setShowSuggestions(true)
    } catch (err) {
      console.error("Error fetching suggestions:", err)
      setSuggestions([])
    }
  }, 300)

  return (
    <div className="w-full flex justify-center relative ">
      <Card className="w-full max-w-5xl rounded-3xl shadow-xl border border-border bg-background">
        <CardContent className="space-y-6 p-8">
          <h2 className="text-2xl font-semibold text-center flex items-center gap-2 justify-center">
            <span role="img" aria-label="search">🔍</span> Search Product
          </h2>

          <form onSubmit={handleSubmit} className="flex flex-col gap-4 md:flex-row md:items-end relative">
            <div className="flex-1 relative">
              <Label htmlFor="keyword">Product Name</Label>
              <Input
                id="keyword"
                placeholder="e.g. solar panel"
                value={keyword}
                onFocus={() => {
                  setSuggestions(allCategories)
                  setShowSuggestions(true)
                }}
                onChange={(e) => {
                  const val = e.target.value
                  setKeyword(val)

                  const filtered = allCategories.filter((cat) =>
                    cat.toLowerCase().includes(val.toLowerCase())
                  )
                  setSuggestions(filtered)
                  setShowSuggestions(true)
                }}
                className="rounded-full px-4 py-2"
              />
              {showSuggestions && suggestions.length > 0 && (
                <ul className="absolute z-50 bg-white text-black mt-1 w-full max-h-60 overflow-y-auto rounded-lg shadow border border-gray-200">
                  {suggestions.map((item, idx) => (
                    <li
                      key={idx}
                      className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                      onClick={() => {
                        setKeyword(item)
                        setShowSuggestions(false)
                      }}
                    >
                      {item}
                    </li>
                  ))}
                </ul>
              )}
            </div>

            <div className="w-32">
              <Label htmlFor="maxCount">Max Results</Label>
              <Select value={maxCount} onValueChange={(val) => setMaxCount(val)}>
                <SelectTrigger className="rounded-full">
                  <SelectValue placeholder="Select max result count" />
                </SelectTrigger>
                <SelectContent>
                  {["3", "5", "10", "20"].map((value) => (
                    <SelectItem key={value} value={value}>{value}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <Button type="submit" className="rounded-full px-6 py-2" disabled={loading}>
              {loading ? "Scraping..." : "Start Scraping"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

export default SearchManager
