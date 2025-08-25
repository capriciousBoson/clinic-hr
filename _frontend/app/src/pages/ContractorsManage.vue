<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getContractors } from "@/typescript/contractors";

import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Eye, Pencil, FileMinus } from "lucide-vue-next";

type Party = {
    phone_number?: string;
    email?: string;
};
type Contractor = { id: number; party?: Party };

const contractors = ref<any[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);


async function load() {
    loading.value = true;
    error.value = null;
    try {
        const data = await getContractors({ page: 1, page_size: 25 });
        contractors.value = Array.isArray(data) ? data : (data.results ?? []);
        console.log (contractors.value); 
    } catch (e: any) {
        error.value = e?.message || "Failed to fetch contractors";
    } finally {
        loading.value = false;
    }
}


onMounted(load);

const selectedId = ref<number | null>(null);
const selectedRow = ref<any | null>(null);

</script>

<template>
    <div class="p-6">
        <p v-if="loading">Loading…</p>
        <p v-else-if="error" class="text-red-600">{{ error }}</p>

        <div v-else class="overflow-auto border rounded-xl">
        <Table>
            <TableHeader>
            <TableRow>
                <TableHead>Contractor Name</TableHead>
                <TableHead>Mobile</TableHead>
                <TableHead>Email</TableHead>
                <TableHead class="text-right">Actions</TableHead>
            </TableRow>
            </TableHeader>

            <TableBody>
            <TableRow v-for="c in contractors" :key="c.id">
                <TableCell>{{ c.contractor_name || "—" }}</TableCell>
                <TableCell>{{ c.party?.phone_number || "—" }}</TableCell>
                <TableCell>{{ c.party?.email || "—" }}</TableCell>
                <TableCell class="text-right">
                <div class="flex items-center justify-end gap-2">
                    <Button variant="ghost" size="sm" class="inline-flex items-center gap-1" @click="onView(e)">
                    <Eye class="w-4 h-4" /><span class="hidden sm:inline">View Details</span>
                    </Button>
                    <Button variant="ghost" size="sm" class="inline-flex items-center gap-1" @click="onEdit(e)">
                    <Pencil class="w-4 h-4" /><span class="hidden sm:inline">Edit Details</span>
                    </Button>
                    <Button variant="destructive" size="sm" class="inline-flex items-center gap-1" @click="Delete(e)">
                    <FileMinus class="w-4 h-4" /><span class="hidden sm:inline">Delete</span>
                    </Button>
                </div>
                </TableCell>
            </TableRow>
            </TableBody>
        </Table>
        </div>
    </div>
</template>

