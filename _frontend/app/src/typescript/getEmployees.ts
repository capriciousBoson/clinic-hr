// src/api.ts
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api", 
});

// GET employees (no body, only query params)
export async function getEmployees(params: Record<string, any> = {}) {
  const res = await api.get("/emp/employeeapi/", { params }); // DRF expects trailing slash
  // If DRF pagination is on -> { count, results, next, previous }
  return res.data;
}

export async function getEmployee(id: number | string) {
  const { data } = await api.get(`/emp/employeeapi/${id}/`);
  return data; // single employee object
}


export async function updateEmployee(id: number | string, payload: any) {
  const { data } = await api.put(`/emp/employeeapi/${id}/`, payload, {
    headers: { "Content-Type": "application/json" },
  });
  return data;
} 


