import { Card, CardContent } from "./ui/card"
import { Label } from "./ui/label"
import { Input } from "./ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select"
import { Button } from "./ui/button"
import { useState } from "react"
import { toast } from "sonner"
import { useEmail } from "../hooks/use-email"

const SearchManager = ({ onSearch, loading }) => {
  const [keyword, setKeyword] = useState("")
  const [maxCount, setMaxCount] = useState("5")
  const { email } = useEmail()

  const handleSubmit = (e) => {
    e.preventDefault()

    if (!keyword.trim()) {
      toast.error("Please enter a product keyword.")
      return
    }

    onSearch({ keyword, maxCount, email })
  }

  return (
    <div className="w-full flex justify-center">
      <Card className="w-full max-w-5xl rounded-3xl shadow-xl border border-border bg-background">
        <CardContent className="space-y-6 p-8">
          <h2 className="text-2xl font-semibold text-center flex items-center gap-2 justify-center">
            <span role="img" aria-label="search">🔍</span> Search Product
          </h2>

          <form onSubmit={handleSubmit} className="flex flex-col gap-4 md:flex-row md:items-end">
            <div className="flex-1">
              <Label htmlFor="keyword" className="text-sm font-medium">Product Name</Label>
              <Input
                id="keyword"
                placeholder="e.g. solar panel"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                className="rounded-full px-4 py-2"
              />
            </div>

            <div className="w-32">
              <Label htmlFor="maxCount" className="text-sm font-medium">Max Results</Label>
              <Select onValueChange={(val) => setMaxCount(val)} defaultValue="5">
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
