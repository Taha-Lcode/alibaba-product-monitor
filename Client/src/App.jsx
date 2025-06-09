import { Outlet } from 'react-router-dom'
import './App.css'
import App_sidebar from './components/App-sidebar'
import { SidebarProvider } from "./components/ui/sidebar"
import { ThemeProvider } from './context/theme-provider'
import { Toaster } from 'sonner'
import { EmailProvider } from './hooks/use-email'

function App() {

  return (
    <div>
      <ThemeProvider defaultTheme='light'>
        <EmailProvider>
          <SidebarProvider>
            <App_sidebar />
            <Outlet />
            <Toaster position="top-center" richColors />
          </SidebarProvider>
        </EmailProvider>
      </ThemeProvider>
    </div>
  )
}

export default App