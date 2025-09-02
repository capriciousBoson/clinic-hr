// src/api.ts
import axios from "axios";

const API_BASE = "/api/";
const api = axios.create({
  baseURL: API_BASE, 
  auth: {
    username: "prabh",
    password: "wasd1234",
  },
});

const s = (v: any) => (typeof v === "string" ? v.trim() : v);
const lower = (v?: string) => (v ? v.toLowerCase().trim() : v);
const addIf = (obj: Record<string, any>, key: string, val: any) => {
  if (val === undefined || val === null) return;
  const str = typeof val === "string" ? val.trim() : val;
  if (str === "" || (typeof str === "number" && Number.isNaN(str))) return;
  obj[key] = str;
};

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
    
        date_offboarded: formValues.date_offboarded ?? current.date_offboarded,

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



export async function createEmployee(formValues: any) {
  // REQUIRED party fields
  const party: Record<string, any> = {
    email: s(formValues.email),
    phone_number: s(formValues.mobile),
    address_state: s(formValues.state),
  };
  // OPTIONAL party fields
  addIf(party, "address_full", s(formValues.address_full));
  addIf(party, "address_city", s(formValues.city));
  addIf(party, "address_zip", s(formValues.address_zip));

  // REQUIRED top-level
  const payload: Record<string, any> = {
    party,
    first_name: s(formValues.firstname),
    last_name: s(formValues.lastname),
    date_hired: s(formValues.employee_hiring_date), // expects YYYY-MM-DD
  };

  // OPTIONAL top-level (only include if provided)
  addIf(payload, "dob", s(formValues.dob)); // YYYY-MM-DD (omit if "")
  if (formValues.gender) payload.gender = lower(formValues.gender);
  if (formValues.ssn) payload.ssn = s(formValues.ssn).replace(/-/g, "");
  if (formValues.compensation_type) payload.compensation_type = lower(formValues.compensation_type);
  if (formValues.marital_status) payload.marital_status = lower(formValues.marital_status);

  if (
    formValues.dependants_count !== undefined &&
    formValues.dependants_count !== null &&
    `${formValues.dependants_count}`.trim() !== ""
  ) {
    payload.dependants = Number(formValues.dependants_count);
  }

  // Offboarding date (optional) — omit if empty string
  addIf(payload, "date_offboarded", s(formValues.date_offboarded));

  // POST
  const { data } = await api.post("/emp/employeeapi/", payload, {
    headers: { "Content-Type": "application/json" },
  });
  return data;
}


