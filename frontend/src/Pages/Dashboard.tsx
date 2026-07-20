import { useQuery } from '@tanstack/react-query'
import { Users, Activity, AlertTriangle, TrendingUp } from 'lucide-react'
import StatCard from '../Components/StatCard'
import RiskDistribution from '../Components/RiskDistribution'
import RecentPatients from '../Components/RecentPatients'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function Dashboard() {
  const { data: stats } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      const res = await axios.get(`${API_URL}/api/v1/patients`)
      return {
        totalPatients: res.data?.length || 0,
        highRisk: 12,
        careGaps: 8,
        avgRisk: 15.3,
      }
    },
  })

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Dashboard</h2>
        <p className="text-gray-500 mt-1">Overview of your patient population</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Patients"
          value={stats?.totalPatients || 0}
          icon={Users}
          trend="+5%"
          trendUp={true}
        />
        <StatCard
          title="High Risk"
          value={stats?.highRisk || 0}
          icon={AlertTriangle}
          trend="-2"
          trendUp={false}
          color="red"
        />
        <StatCard
          title="Care Gaps"
          value={stats?.careGaps || 0}
          icon={Activity}
          trend="+3"
          trendUp={false}
          color="orange"
        />
        <StatCard
          title="Avg Risk Score"
          value={`${stats?.avgRisk || 0}%`}
          icon={TrendingUp}
          trend="-1.2%"
          trendUp={true}
          color="green"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RiskDistribution />
        <RecentPatients />
      </div>
    </div>
  )
}
