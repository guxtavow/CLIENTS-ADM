export interface UserPreferences {
    timezone: string
  }
  
  export interface User {
    _vts?: number
    active: boolean
    created_ts: string
    isTrusted?: boolean
    last_updated_at: string
    password: string
    preferences: UserPreferences
    roles: string[]
    username: string
  }
  
  export interface UserFormData {
    username: string
    password: string
    active: boolean
    roles: string[]
    preferences: {
      timezone: string
    }
  }