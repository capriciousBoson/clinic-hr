<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { getContractor } from "@/typescript/contractors";

import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";


type Party = {
    email?: string; phone_number?: string;
    address_full?: string | null; address_city?: string | null; address_state?: string ; address_zip?: string | null;
};

type Contractor = {
    id: number;
    party?: Party;
    tin?: string | null;
    contractor_name ?: string;
};

const props = defineProps<{
    open: boolean;
    contractorId: number | null;
    initial?: Contractor | null; // optional seed from the row
}>();

const emit = defineEmits<{
    (e: "update:open", v: boolean): void;
    (e: "edit", id: number): void;
    (e: "delete", id: number): void;
}>();

const loading = ref(false);
const error = ref<string | null>(null);
const data = ref<Contractor | null>(null);

const contractor = computed(() => data.value ?? props.initial ?? null);


async function fetchById(id: number) {
    loading.value = true; error.value = null;
    try {
        data.value = await getContractor(id);
    } catch (e: any) {
        error.value = e?.message || "Failed to load contractor";
    } finally {
        loading.value = false;
    }
}

watch(
    () => [props.open, props.contractorId],
    async ([open, id], [prevOpen, prevId]) => {
        if (open && id && (id !== prevId || !data.value)) {
        await fetchById(id);
        }
    },
    { immediate: true }
);


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
    if (!contractor.value) return [];
    const c = contractor.value;
    return [
        ["ID", c.id],
        ["Contractor Name", c.contractor_name],
        ["Taxpayer Identification Number", c.tin],
        ["Email", c.party?.email],
        ["Mobile", c.party?.phone_number],
        ["Address", c.party?.address_full],
        ["City", c.party?.address_city],
        ["State", c.party?.address_state],
        ["ZIP", c.party?.address_zip],
    ];
});
</script>
<template>
    <Dialog :open="open" @update:open="v => emit('update:open', v)">
        <DialogContent class="sm:max-w-2xl" :key="contractorId">
        <DialogHeader>
            <DialogTitle>Contractor details</DialogTitle>
            <DialogDescription v-if="contractor">
            {{ contractor.contractor_name }} • {{ contractor.party?.email || "—" }}
            </DialogDescription>
        </DialogHeader>

        <div v-if="loading" class="p-4 text-sm text-muted-foreground">Loading…</div>
        <div v-else-if="error" class="p-4 text-sm text-red-600">{{ error }}</div>

        <Card v-else-if="contractor">
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
            <Button variant="outline" @click="contractor?.id && emit('edit', contractor.id)">Edit</Button>
            <Button variant="destructive" @click="contractor?.id && emit('delete', contractor.id)">Offboard</Button>
            </CardFooter>
        </Card>

        <div v-else class="p-4 text-sm text-muted-foreground">No data.</div>
        </DialogContent>
    </Dialog>
</template>