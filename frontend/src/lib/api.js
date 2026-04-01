import axios from "axios"

const API = "http://localhost:8000"

export const generateContent = async (input) => {
  const res = await axios.post(`${API}/generate`, { input })
  return res.data
}