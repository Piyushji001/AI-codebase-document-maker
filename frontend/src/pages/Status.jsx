import { useQuery } from '@tanstack/react-query'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import { CheckCircle2, Circle, Loader2, FileText, Download } from 'lucide-react'

const STEPS = [
  { id: 'queued', label: 'Queued' },
  { id: 'cloning', label: 'Cloning Repository' },
  { id: 'parsing', label: 'Analyzing Structure' },
  { id: 'generating', label: 'AI Generating Docs' },
  { id: 'building', label: 'Building Site' },
  { id: 'uploading', label: 'Uploading Artifacts' },
  { id: 'completed', label: 'Done' }
]

export default function Status() {
  const { jobId } = useParams()
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  const { data, error, isError } = useQuery({
    queryKey: ['jobStatus', jobId],
    queryFn: async () => {
      const res = await axios.get(`${API_URL}/job-status/${jobId}`)
      return res.data
    },
    refetchInterval: (data) => (data?.status === 'completed' || data?.status === 'failed' ? false : 2000),
  })

  const currentStatus = data?.status || 'queued'
  const currentStepIndex = STEPS.findIndex(s => s.id === currentStatus)
  const isFailed = currentStatus === 'failed'

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white shadow-xl rounded-2xl overflow-hidden">
          <div className="px-6 py-8 sm:p-10 border-b border-gray-100">
            <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-3">
              <FileText className="w-8 h-8 text-blue-600" />
              Documentation Status
            </h2>
            <p className="mt-2 text-gray-500">
              Job ID: <span className="font-mono text-xs bg-gray-100 px-2 py-1 rounded">{jobId}</span>
            </p>
          </div>

          <div className="px-6 py-8 sm:p-10 space-y-8">
            {isError && (
               <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                 Error loading status: {error.message}
               </div>
            )}

            {isFailed && (
               <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                 Job Failed: {data?.message}
               </div>
            )}

            <div className="space-y-6">
              {STEPS.map((step, index) => {
                const isCompleted = currentStepIndex > index || currentStatus === 'completed'
                const isCurrent = currentStatus === step.id
                
                return (
                  <div key={step.id} className="flex items-center gap-4">
                    <div className="flex-none">
                      {isCompleted ? (
                        <CheckCircle2 className="w-6 h-6 text-green-500" />
                      ) : isCurrent ? (
                        <Loader2 className="w-6 h-6 text-blue-600 animate-spin" />
                      ) : (
                        <Circle className="w-6 h-6 text-gray-300" />
                      )}
                    </div>
                    <div className={`flex-1 ${isCurrent ? 'font-semibold text-gray-900' : 'text-gray-500'}`}>
                      {step.label}
                    </div>
                  </div>
                )
              })}
            </div>

            {currentStatus === 'completed' && data?.download_url && (
              <div className="mt-8 pt-8 border-t border-gray-100">
                <a
                  href={data.download_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full flex items-center justify-center gap-2 bg-green-600 text-white px-6 py-4 rounded-xl font-semibold hover:bg-green-500 transition-colors shadow-lg shadow-green-200"
                >
                  <Download className="w-5 h-5" />
                  Download Documentation
                </a>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
