import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL, 
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
        address_state: (s(formValues.address_state) || "").toUpperCase(),
    }

    // OPTIONAL party fields
    addIf(party, "address_full", s(formValues.address_full))
    addIf(party, "address_city", s(formValues.address_city))
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

export async function getContractor(id: number | string) {
    const { data } = await api.get(`/emp/contractorapi/${id}/`);
    return data; 
}

export async function updateContractor(
    id: number | string,
    formValues: any,
    baseline?: any 
) {
    const current = baseline ?? (await api.get(`/emp/contractorapi/${id}/`)).data;


    const payload = {
        // top-level employee fields
        contractor_name: formValues.contractor_name ?? current.contractor_name,
        tin: formValues.tin ? String(formValues.tin).replace(/-/g, "") : current.tin,

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

    const { data } = await api.put(`/emp/contractorapi/${id}/`, payload); // note the trailing slash
    return data;
}
