<script setup lang="ts">
import { ref, onMounted } from "vue";
// adjust path if you don't use '@' alias
import { getEmployees } from "@/typescript/getEmployees";


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



onMounted(load);

</script>