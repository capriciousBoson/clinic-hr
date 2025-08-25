<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { getEmployee } from "@/typescript/employees";

import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

type Party = {
    first_name?: string; last_name?: string; email?: string; phone_number?: string;
    dob?: string | null; gender?: string | null;
    address_full?: string | null; address_city?: string | null; address_state?: string | null; address_zip?: string | null;
};
type Employee = {
    id: number;
    party?: Party;
    compensation_type?: string | null;
    date_hired?: string | null;
    date_offboarded?: string | null;
};

const props = defineProps<{
    open: boolean;
    employeeId: number | null;
    initial?: Employee | null; // optional seed from the row
}>();

const emit = defineEmits<{
    (e: "update:open", v: boolean): void;
    (e: "edit", id: number): void;
    (e: "offboard", id: number): void;
}>();

const loading = ref(false);
const error = ref<string | null>(null);
const data = ref<Employee | null>(null);

const emp = computed(() => data.value ?? props.initial ?? null);

function titleCase(x?: string | null) {
    if (!x) return "—";
    const s = x.trim();
    return s ? s[0].toUpperCase() + s.slice(1).toLowerCase() : "—";
}
function fmtDate(s?: string | null) {
    if (!s) return "—";
    const d = new Date(s);
    return isNaN(+d) ? s : d.toLocaleDateString();
}

async function fetchById(id: number) {
    loading.value = true; error.value = null;
    try {
        data.value = await getEmployee(id);
    } catch (e: any) {
        error.value = e?.message || "Failed to load employee";
    } finally {
        loading.value = false;
    }
}

watch(
    () => [props.open, props.employeeId],
    async ([open, id], [prevOpen, prevId]) => {
        if (open && id && (id !== prevId || !data.value)) {
        await fetchById(id);
        }
    },
    { immediate: true }
);

// tiny inline field component
const Labeled = {
    props: { label: String, value: [String, Number] },
    template: `
        <div>
        <div class="text-xs text-muted-foreground">{{ label }}</div>
        <div class="mt-1 font-medium">{{ value ?? "—" }}</div>
        </div>
    `
};


const details = computed<[string, any][]>(() => {
    if (!emp.value) return [];
    const e = emp.value;
    return [
        ["ID", e.id],
        ["First name", e.first_name],
        ["Last name", e.last_name],
        ["Email", e.party?.email],
        ["Mobile", e.party?.phone_number],
        ["DOB", fmtDate(e.dob)],
        ["Date started", fmtDate(e.date_hired)],
        ["Gender", titleCase(e.gender)],
        ["Payment type", titleCase(e.compensation_type)],
        ["Address", e.party?.address_full],
        ["City", e.party?.address_city],
        ["State", e.party?.address_state],
        ["ZIP", e.party?.address_zip],
        ["Date offboarded", fmtDate(e.date_offboarded)],
    ];
});


</script>

<template>
    <Dialog :open="open" @update:open="v => emit('update:open', v)">
        <DialogContent class="sm:max-w-2xl" :key="employeeId">
        <DialogHeader>
            <DialogTitle>Employee details</DialogTitle>
            <DialogDescription v-if="emp">
            {{ emp.party?.first_name }} {{ emp.party?.last_name }} • {{ emp.party?.email || "—" }}
            </DialogDescription>
        </DialogHeader>

        <div v-if="loading" class="p-4 text-sm text-muted-foreground">Loading…</div>
        <div v-else-if="error" class="p-4 text-sm text-red-600">{{ error }}</div>

        <Card v-else-if="emp">
            <CardContent class="p-4">
                <dl class="space-y-2">
                <div
                    v-for="([label, value], i) in details"
                    :key="i"
                    class="flex gap-3"
                >
                    <dt class="w-48 shrink-0 text-xs text-muted-foreground">{{ label }}</dt>
                    <dd class="flex-1 font-medium break-words">{{ value ?? "—" }}</dd>
                </div>
                </dl>
            </CardContent>

            <CardFooter class="justify-end gap-2">
            <Button variant="ghost" @click="emit('update:open', false)">Close</Button>
            <Button variant="outline" @click="emp?.id && emit('edit', emp.id)">Edit</Button>
            <Button variant="destructive" @click="emp?.id && emit('offboard', emp.id)">Offboard</Button>
            </CardFooter>
        </Card>

        <div v-else class="p-4 text-sm text-muted-foreground">No data.</div>
        </DialogContent>
    </Dialog>
</template>