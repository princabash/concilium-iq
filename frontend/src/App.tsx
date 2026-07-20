import { Routes, Route } from 'react-router-dom'
import Layout from './Layout/Layout'
import Dashboard from './Pages/Dashboard'
import PatientList from './Pages/PatientList'
import PatientDetail from './Pages/PatientDetail'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/patients" element={<PatientList />} />
        <Route path="/patients/:id" element={<PatientDetail />} />
      </Routes>
    </Layout>
  )
}

export default App
