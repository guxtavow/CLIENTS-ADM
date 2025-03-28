import axios, { type AxiosResponse } from 'axios'
import type { User, UserFormData } from '@/interface/user.interface'

const API_BASE_URL = 'http://localhost:5000' // Your Flask backend URL

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default {
  async getUsers(): Promise<User[]> {
    try {
      const response: AxiosResponse<User[]> = await api.get('/users')
      return response.data
    } catch (error) {
      console.error('Error fetching users:', error)
      throw error
    }
  },

  async getUser(username: string): Promise<User | undefined> {
    try {
      const response: AxiosResponse<User[]> = await api.get('/users')
      return response.data.find((user: User) => user.username === username)
    } catch (error) {
      console.error('Error fetching user:', error)
      throw error
    }
  },

  async createUser(userData: UserFormData): Promise<User> {
    try {
      const response = await axios.post('/new_users', userData, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error creating user:', error);
      throw error;
    }
  },

  async updateUser(username: string, userData: Partial<UserFormData>): Promise<User> {
    try {
      const response: AxiosResponse<User> = await api.put(`/update_users/${username}`, userData)
      return response.data
    } catch (error) {
      console.error('Error updating user:', error)
      throw error
    }
  },

  async deleteUser(username: string): Promise<void> {
    try {
      await api.delete(`/users/${username}`)
    } catch (error) {
      console.error('Error deleting user:', error)
      throw error
    }
  },
}