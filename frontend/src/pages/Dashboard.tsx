import Navbar from '../components/Navbar'

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-3xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-2" data-testid="dashboard-heading">
          Dashboard
        </h1>
        <p className="text-gray-500">
          You are logged in. Item management coming in the next story (EPMCDMETST-55184).
        </p>
      </main>
    </div>
  )
}
