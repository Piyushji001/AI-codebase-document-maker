import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { Github, ArrowRight, Loader2 } from 'lucide-react'

export default function Home() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      // In dev, we might need to point to localhost:8000 explicitly if proxy isn't set
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      
      const response = await axios.post(`${API_URL}/start-documentation`, {
        repo_url: url
      })

      const { job_id } = response.data
      navigate(`/status/${job_id}`)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start documentation job')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <div className="max-w-2xl w-full text-center space-y-8">
        <div className="space-y-4">
          <div className="flex justify-center">
            <div className="p-4 bg-blue-600 rounded-2xl shadow-lg shadow-blue-200">
              <Github className="w-12 h-12 text-white" />
            </div>
          </div>
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
            Autonomous Codebase Documenter
          </h1>
          <p className="text-lg leading-8 text-gray-600">
            Turn any GitHub repository into comprehensive documentation in minutes using AI.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="mt-10 max-w-xl mx-auto">
          <div className="flex gap-x-4">
            <input
              type="url"
              required
              placeholder="https://github.com/username/repo"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="min-w-0 flex-auto rounded-xl border-0 px-4 py-3.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6"
            />
            <button
              type="submit"
              disabled={loading}
              className="flex-none rounded-xl bg-blue-600 px-6 py-3.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              {loading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <div className="flex items-center gap-2">
                  Generate <ArrowRight className="w-4 h-4" />
                </div>
              )}
            </button>
          </div>
          {error && (
            <p className="mt-4 text-sm text-red-600 bg-red-50 py-2 px-4 rounded-lg inline-block">
              {error}
            </p>
          )}
        </form>
      </div>
    </div>
  )
}
