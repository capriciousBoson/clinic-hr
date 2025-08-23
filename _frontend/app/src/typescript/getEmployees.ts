// src/api.ts
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api", 
  auth: {
    username: "prabh",
    password: "wasd1234",
  },
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


export async function updateEmployee(
  id: number | string,
  formValues: any,
  baseline?: any // pass the already-fetched employee to avoid an extra GET
) {
  const current = baseline ?? (await api.get(`/emp/employeeapi/${id}/`)).data;

  // lowercase helper
  const lower = (v?: string) => (v ? v.toLowerCase() : v);

  // Build a FULL payload the server accepts (merge changes onto current)
  const payload = {
    // top-level employee fields
    first_name: formValues.firstname ?? current.first_name,
    last_name: formValues.lastname ?? current.last_name,
    dob: formValues.dob ?? current.dob,
    gender: formValues.gender ? lower(formValues.gender) : current.gender,
    ssn: formValues.ssn ? String(formValues.ssn).replace(/-/g, "") : current.ssn,
    compensation_type: formValues.compensation_type
      ? lower(formValues.compensation_type)
      : current.compensation_type,
    date_hired: formValues.employee_hiring_date ?? current.date_hired,
    marital_status: formValues.marital_status
      ? lower(formValues.marital_status)
      : current.marital_status,
    dependants:
      formValues.dependants_count !== undefined &&
      formValues.dependants_count !== null &&
      `${formValues.dependants_count}`.trim() !== ""
        ? Number(formValues.dependants_count)
        : current.dependants,
    date_offboarded: current.date_offboarded ?? null, // keep existing unless you change it

    // nested party
    party: {
      ...(current.party ?? {}),
      email: formValues.email ?? current.party?.email,
      phone_number: formValues.mobile ?? current.party?.phone_number,
      address_full: formValues.address_full ?? current.party?.address_full,
      address_city: formValues.city ?? current.party?.address_city,
      address_state: formValues.state ?? current.party?.address_state,
      address_zip: formValues.address_zip ?? current.party?.address_zip,
    },
  };

  const { data } = await api.put(`/emp/employeeapi/${id}/`, payload); // note the trailing slash
  return data;
}


