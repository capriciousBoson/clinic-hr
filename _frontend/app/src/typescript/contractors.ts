import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000/api", 
    auth: {
        username: "prabh",
        password: "wasd1234",
    },
});

const s = (v: any) => (typeof v === "string" ? v.trim() : v);
const addIf = (obj: Record<string, any>, key: string, val: any) => {
    if (val === undefined || val === null) return;
    const str = typeof val === "string" ? val.trim() : val;
    if (str === "" || (typeof str === "number" && Number.isNaN(str))) return;
    obj[key] = str;
};

export async function createContractor(formValues: any) {
    const party: Record<string, any> = {
        email: s(formValues.email),
        phone_number: s(formValues.phone_number),
        address_state: (s(formValues.state) || "").toUpperCase(),
    }

    // OPTIONAL party fields
    addIf(party, "address_full", s(formValues.address_full))
    addIf(party, "address_city", s(formValues.city))
    addIf(party, "address_zip", s(formValues.address_zip))

    const payload: Record<string, any> = {
        party,
        contractor_name: s(formValues.contractor_name),
        tin: String(s(formValues.tin) ?? "").replace(/\D/g, ""),
    }

    const { data } = await api.post("/emp/contractorapi/", payload, {
        headers: { "Content-Type": "application/json" },
    })
    return data
}

export async function getContractors(params: Record<string, any> = {}) {
  const res = await api.get("/emp/contractorapi/", { params }); // DRF expects trailing slash
  // If DRF pagination is on -> { count, results, next, previous }
  return res.data;
}