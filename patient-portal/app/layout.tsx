export const metadata = {
  title: 'Concilium IQ - Patient Portal',
  description: 'Your personal clinical intelligence dashboard',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50">{children}</body>
    </html>
  )
}
