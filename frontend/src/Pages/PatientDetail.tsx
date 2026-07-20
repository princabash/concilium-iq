import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { ArrowLeft, Heart, Activity, FlaskConical } from 'lucide-react'
import { Link } from 'react-router-dom'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function PatientDetail() {
  const { id } = useParams<{ id: string }>()

  const { data: summary, isLoading } = useQuery({
    queryKey: ['patient-summary', id],
    queryFn: async () => {
      const res = await axios.get(`${API_URL}/api/v1/summary/${id}`)
      return res.data
    },
    enabled: !!id,
  })

  if (isLoading) {
    return <div className="text-center py-12">Loading patient data...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <Link to="/patients" className="text-gray-500 hover:text-gray-700">
          <ArrowLeft className="w-5 h-5" />
        </Link>
        <div>
          <h2 className="text-2xl font-bold text-gray-900">
            Patient {id}
          </h2>
          <p className="text-gray-500">Clinical Intelligence Summary</p>
        </div>
      </div>

      {summary ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Risk Card */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center mb-4">
              <Heart className="w-5 h-5 text-red-500 mr-2" />
              <h3 className="text-lg font-semibold">Risk Profile</h3>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-500">Category</span>
                <span className={`font-medium capitalize ${
                  summary.risk?.risk_category === 'very_high' ? 'text-red-600' :
                  summary.risk?.risk_category === 'high' ? 'text-orange-600' :
                  'text-green-600'
                }`}>
                  {summary.risk?.risk_category?.replace('_', ' ')}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">LDL Target</span>
                <span className="font-medium">{summary.risk?.ldl_target_mgdl} mg/dL</span>
              </div>
            </div>
          </div>

          {/* Labs Card */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center mb-4">
              <FlaskConical className="w-5 h-5 text-blue-500 mr-2" />
              <h3 className="text-lg font-semibold">Latest Labs</h3>
            </div>
            <div className="space-y-3">
              {summary.latest_labs?.ldl_c && (
                <div className="flex justify-between">
                  <span className="text-gray-500">LDL-C</span>
                  <span className="font-medium">{summary.latest_labs.ldl_c.value} mg/dL</span>
                </div>
              )}
              {summary.latest_labs?.apob && (
                <div className="flex justify-between">
                  <span className="text-gray-500">ApoB</span>
                  <span className="font-medium">{summary.latest_labs.apob.value} mg/dL</span>
                </div>
              )}
              {summary.latest_labs?.hba1c && (
                <div className="flex justify-between">
                  <span className="text-gray-500">HbA1c</span>
                  <span className="font-medium">{summary.latest_labs.hba1c.value}%</span>
                </div>
              )}
            </div>
          </div>

          {/* Care Gaps Card */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center mb-4">
              <Activity className="w-5 h-5 text-orange-500 mr-2" />
              <h3 className="text-lg font-semibold">Care Gaps</h3>
            </div>
            <div className="space-y-2">
              {summary.care_gaps?.map((gap: any, idx: number) => (
                <div key={idx} className="p-3 bg-orange-50 rounded-lg">
                  <p className="text-sm font-medium text-orange-800">{gap.description}</p>
                  <p className="text-xs text-orange-600 mt-1">{gap.guideline_reference}</p>
                </div>
              )) || <p className="text-gray-500 text-sm">No care gaps identified</p>}
            </div>
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <p className="text-gray-500">No summary available for this patient</p>
        </div>
      )}
    </div>
  )
}
