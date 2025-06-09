import { LayoutDashboard, Moon, Sun, Warehouse, Mail, Settings2 } from "lucide-react"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu, SidebarMenuButton, SidebarMenuItem
} from "./ui/sidebar"
import { Link } from "react-router-dom"
import { useTheme } from "../context/theme-provider"
import { useState, useEffect } from "react"
import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar"
import { Input } from "./ui/input"
import { useEmail } from "../hooks/use-email"
import { Switch } from "./ui/switch"
import { Popover, PopoverContent, PopoverTrigger } from "./ui/popover"
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "./ui/select"
import { toast } from "sonner"

const items = [
  {
    title: "Dashboard",
    url: "/",
    icon: LayoutDashboard,
  },
  {
    title: "Products",
    url: "/products",
    icon: Warehouse,
  },
]

const App_sidebar = () => {
  const { theme, setTheme } = useTheme()
  const isDark = theme === "dark"

  const { email, setEmail } = useEmail()
  const [editing, setEditing] = useState(false)
  const [showSettings, setShowSettings] = useState(false)
  const [notificationsEnabled, setNotificationsEnabled] = useState(false)
  const [schedulerEnabled, setSchedulerEnabled] = useState(false)
  const [scheduleTime, setScheduleTime] = useState("09:00")

  useEffect(() => {
    if (notificationsEnabled && !email) {
      toast.warning("Please set your email address to receive notifications.")
    }
  }, [notificationsEnabled, email])

  return (
    <Sidebar className="items-center">
      <SidebarHeader>
        <div
          onClick={() => setTheme(isDark ? "light" : "dark")}
          className={`flex items-center cursor-pointer transition-transform duration-500 w-fit ${isDark ? "rotate-180" : "rotate-0"}`}
        >
          {isDark ? (
            <Sun className='h-7 w-7 text-yellow-500 rotate-0 transition-all' />
          ) : (
            <Moon className='h-7 w-7 text-blue-500 rotate-0 transition-all' />
          )}
        </div>
      </SidebarHeader>

      <SidebarContent className="flex-1 flex flex-col justify-center">
        <SidebarMenu>
          {items.map((item) => (
            <SidebarMenuItem key={item.title}>
              <SidebarMenuButton asChild>
                <Link to={item.url} className="flex items-center gap-2">
                  <item.icon className="w-5 h-5" />
                  <span>{item.title}</span>
                </Link>
              </SidebarMenuButton>
            </SidebarMenuItem>
          ))}

          <SidebarMenuItem>
            <Popover open={showSettings} onOpenChange={setShowSettings}>
              <PopoverTrigger asChild>
                <SidebarMenuButton className="flex items-center gap-2 cursor-pointer">
                  <Settings2 className="w-5 h-5" />
                  <span>Settings</span>
                </SidebarMenuButton>
              </PopoverTrigger>
              <PopoverContent className="w-80 space-y-4 p-4">
                <h4 className="text-md font-medium">Settings</h4>

                <div className="flex items-center justify-between">
                  <span>Notifications</span>
                  <Switch
                    checked={notificationsEnabled}
                    onCheckedChange={setNotificationsEnabled}
                    className="cursor-pointer"
                  />
                </div>

                <div className="flex items-center justify-between">
                  <span>Scheduler</span>
                  <Switch
                    checked={schedulerEnabled}
                    onCheckedChange={setSchedulerEnabled}
                    className="cursor-pointer"
                  />
                </div>

                {schedulerEnabled && (
                  <div className="space-y-1">
                    <label className="text-sm">Schedule Time</label>
                    <Select onValueChange={setScheduleTime} defaultValue={scheduleTime}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select time" />
                      </SelectTrigger>
                      <SelectContent>
                        {["06:00", "09:00", "12:00", "15:00", "18:00", "21:00"].map((time) => (
                          <SelectItem key={time} value={time}>{time}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                )}
              </PopoverContent>
            </Popover>
          </SidebarMenuItem>

        </SidebarMenu>
      </SidebarContent>

      <SidebarFooter className="p-4 w-full">
        <div className="flex items-center gap-3">
          <Avatar className="h-9 w-9">
            <AvatarImage
              src={`https://api.dicebear.com/7.x/initials/svg?seed=${email || 'U'}`}
              alt="Profile"
            />
            <AvatarFallback>U</AvatarFallback>
          </Avatar>

          {editing ? (
            <form
              onSubmit={(e) => {
                e.preventDefault()
                setEditing(false)
              }}
              className="flex-1"
            >
              <Input
                type="email"
                placeholder="Enter email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="h-9 text-sm px-3 py-1"
              />
            </form>
          ) : (
            <button
              className="text-sm text-muted-foreground hover:text-primary text-left truncate"
              onClick={() => setEditing(true)}
            >
              <div className="flex items-center gap-2">
                <Mail className="w-4 h-4" />
                <span>{email || "Set email"}</span>
              </div>
            </button>
          )}
        </div>
      </SidebarFooter>
    </Sidebar>
  )
}

export default App_sidebar
