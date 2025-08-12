<script setup lang="ts">
import { ref, onMounted } from "vue";
// adjust path if you don't use '@' alias
import { getEmployees } from "@/typescript/getEmployees";


import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Eye, Pencil, UserMinus } from "lucide-vue-next";
import EmployeeDetailsCard from "@/pages/EmployeeDetailsCard.vue";


type Party = {
    first_name?: string;
    last_name?: string;
    phone_number?: string;
    email?: string;
};
type Employee = { id: number; party?: Party };


const employees = ref<any[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

async function load() {
    loading.value = true;
    error.value = null;
    try {
        const data = await getEmployees({ page: 1, page_size: 25 });
        employees.value = Array.isArray(data) ? data : (data.results ?? []);
        console.log (employees.value); 
    } catch (e: any) {
        error.value = e?.message || "Failed to fetch employees";
    } finally {
        loading.value = false;
    }
}

function fmtString(g?: string | null) {
    if (!g) return "—";
    const t = g.toString().trim();
    return t.charAt(0).toUpperCase() + t.slice(1).toLowerCase();
}


onMounted(load);


const showDetails = ref(false);
const selectedId = ref<number | null>(null);
const selectedRow = ref<any | null>(null);

function onView(row: any) {
    if (!row?.id) return;
    selectedId.value = Number(row.id);
    selectedRow.value = row;        // optional seed
    showDetails.value = true;
}

</script>

<template>
    <div class="p-6">
        <p v-if="loading">Loading…</p>
        <p v-else-if="error" class="text-red-600">{{ error }}</p>

        <div v-else class="overflow-auto border rounded-xl">
        <Table>
            <TableHeader>
            <TableRow>
                <TableHead>First name</TableHead>
                <TableHead>Last name</TableHead>
                <TableHead>Mobile</TableHead>
                <TableHead>Email</TableHead>
                <TableHead>Employment Start Date</TableHead>
                <TableHead>Gender</TableHead>
                <TableHead>Compensation Type</TableHead>
                <TableHead class="text-right">Actions</TableHead>
            </TableRow>
            </TableHeader>

            <TableBody>
            <TableRow v-for="e in employees" :key="e.id">
                <TableCell>{{ e.party?.first_name || "—" }}</TableCell>
                <TableCell>{{ e.party?.last_name || "—" }}</TableCell>
                <TableCell>{{ e.party?.phone_number || "—" }}</TableCell>
                <TableCell>{{ e.party?.email || "—" }}</TableCell>
                <TableCell class="whitespace-nowrap">{{ e.date_hired }}</TableCell>
                <TableCell>{{ fmtString(e.party?.gender) }}</TableCell>
                <TableCell>{{ fmtString(e.compensation_type) || "—" }}</TableCell>
                <TableCell class="text-right">
                <div class="flex items-center justify-end gap-2">
                    <Button variant="ghost" size="sm" class="inline-flex items-center gap-1" @click="onView(e)">
                    <Eye class="w-4 h-4" /><span class="hidden sm:inline">View Details</span>
                    </Button>
                    <Button variant="ghost" size="sm" class="inline-flex items-center gap-1" @click="onEdit(e.id)">
                    <Pencil class="w-4 h-4" /><span class="hidden sm:inline">Edit Details</span>
                    </Button>
                    <Button variant="destructive" size="sm" class="inline-flex items-center gap-1" @click="onOffboard(e.id)">
                    <UserMinus class="w-4 h-4" /><span class="hidden sm:inline">Offboard</span>
                    </Button>
                </div>
                </TableCell>
            </TableRow>
            </TableBody>
        </Table>
        </div>
    </div>

    <EmployeeDetailsCard
        v-model:open="showDetails"
        :employee-id="selectedId"
        :initial="selectedRow"
    />
</template>