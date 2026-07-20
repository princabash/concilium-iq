import { Link, useLocation } from 'react-router-dom'
import { LayoutDashboard, Users, Activity, Settings } from 'lucide-react'
import clsx from 'clsx'

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Patients', href: '/patients', icon: Users },
  { name: 'Analytics', href: '/analytics', icon: Activity },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export default function Sidebar() {
  const location = useLocation()

  return (
    <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
      <div className="p-6">
        <h1 className="text-xl font-bold text-primary-600">Concilium IQ™</h1>
        <p className="text-xs text-gray-500 mt-1">Clinical Intelligence</p>
      </div>
      <nav className="flex-1 px-4 space-y-1">
        {navigation.map((item) => (
          <Link
            key={item.name}
            to={item.href}
            className={clsx(
              'flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors',
              location.pathname === item.href
                ? 'bg-primary-50 text-primary-700'
                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
            )}
          >
            <item.icon className="w-5 h-5 mr-3" />
            {item.name}
          </Link>
        ))}
      </nav>
      <div className="p-4 border-t border-gray-200">
        <div className="flex items-center">
          <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center">
            <span className="text-sm font-medium text-primary-700">Dr</span>
          </div>
          <div className="ml-3">
            <p className="text-sm font-medium text-gray-900">Dr. Smith</p>
            <p className="text-xs text-gray-500">Cardiologist</p>
          </div>
        </div>
      </div>
    </div>
  )
}
