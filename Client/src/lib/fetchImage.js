export async function fetchImageForKeyword(keyword) {
  const key = import.meta.env.VITE_UNSPLASH_ACCESS_KEY
  const url = `https://api.unsplash.com/search/photos?query=${encodeURIComponent(keyword)}&client_id=${key}&per_page=1`

  try {
    const res = await fetch(url)
    const data = await res.json()
    return data?.results?.[0]?.urls?.regular || null
  } catch (err) {
    console.error("Failed to fetch image:", err)
    return null
  }
}