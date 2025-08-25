<script setup lang="ts">
import { ref, watch, computed } from "vue";
import { getEmployee, updateEmployee } from "@/typescript/employees";
import RequiredLabel from '@/components/ui/required-label.vue'

import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

import {
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from '@/components/ui/form'

import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'


import {
    NumberField,
    NumberFieldContent,
    NumberFieldDecrement,
    NumberFieldIncrement,
    NumberFieldInput,
} from '@/components/ui/number-field'

import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";
import * as z from "zod";


const usStates = [
    { code: "AL", name: "Alabama" },
    { code: "AK", name: "Alaska" },
    { code: "AZ", name: "Arizona" },
    { code: "AR", name: "Arkansas" },
    { code: "CA", name: "California" },
    { code: "CO", name: "Colorado" },
    { code: "CT", name: "Connecticut" },
    { code: "DE", name: "Delaware" },
    { code: "FL", name: "Florida" },
    { code: "GA", name: "Georgia" },
    { code: "HI", name: "Hawaii" },
    { code: "ID", name: "Idaho" },
    { code: "IL", name: "Illinois" },
    { code: "IN", name: "Indiana" },
    { code: "IA", name: "Iowa" },
    { code: "KS", name: "Kansas" },
    { code: "KY", name: "Kentucky" },
    { code: "LA", name: "Louisiana" },
    { code: "ME", name: "Maine" },
    { code: "MD", name: "Maryland" },
    { code: "MA", name: "Massachusetts" },
    { code: "MI", name: "Michigan" },
    { code: "MN", name: "Minnesota" },
    { code: "MS", name: "Mississippi" },
    { code: "MO", name: "Missouri" },
    { code: "MT", name: "Montana" },
    { code: "NE", name: "Nebraska" },
    { code: "NV", name: "Nevada" },
    { code: "NH", name: "New Hampshire" },
    { code: "NJ", name: "New Jersey" },
    { code: "NM", name: "New Mexico" },
    { code: "NY", name: "New York" },
    { code: "NC", name: "North Carolina" },
    { code: "ND", name: "North Dakota" },
    { code: "OH", name: "Ohio" },
    { code: "OK", name: "Oklahoma" },
    { code: "OR", name: "Oregon" },
    { code: "PA", name: "Pennsylvania" },
    { code: "RI", name: "Rhode Island" },
    { code: "SC", name: "South Carolina" },
    { code: "SD", name: "South Dakota" },
    { code: "TN", name: "Tennessee" },
    { code: "TX", name: "Texas" },
    { code: "UT", name: "Utah" },
    { code: "VT", name: "Vermont" },
    { code: "VA", name: "Virginia" },
    { code: "WA", name: "Washington" },
    { code: "WV", name: "West Virginia" },
    { code: "WI", name: "Wisconsin" },
    { code: "WY", name: "Wyoming" }
]



function titleCase(x?: string | null) {
    if (!x) return "—";
    const s = x.trim();
    return s ? s[0].toUpperCase() + s.slice(1).toLowerCase() : "—";
}

type Party = {
  first_name?: string | null;
  last_name?: string | null;
  email?: string | null;
  gender?: string | null;
  dob?: string | null;
  mobile?: mobile | null;
  ssn?: ssn | null;
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
  initial?: Employee | null;
}>();

const emit = defineEmits<{
  (e: "update:open", v: boolean): void;
  (e: "save", payload: any): void;     // you’ll send your form data back
  (e: "cancel"): void;
}>();

const schema = toTypedSchema(
  z.object({
    firstname: z.string().min(1, "First name is required"),
    lastname: z.string().min(1, "Last name is required"),
    gender: z.enum(["Male", "Female", "Other"], {
        errorMap: () => ({ message: "Select valid Gender." })
    }),
    marital_status: z.enum(["Single", "Married", "Divorced"], {
        errorMap: () => ({ message: "Select a valid marital status." })
    }),
    dob: z.string().min(0, "DOB is required"),
    mobile: z.string().regex(/^(\+1)?[2-9]\d{2}[2-9](?!11)\d{6}$/, "Invalid US mobile number"),
    email: z.string().email("Invalid email address"),
    dependants_count: z.coerce.number().int().min(0).max(10).default(0),
    ssn: z.string().regex(/^\d{3}-\d{2}-\d{4}$/, "SSN must be XXX-XX-XXXX"),
    compensation_type: z.enum(["Salaried", "Hourly"], {
        required_error: "Compensation type is required"
    }),
    address_full: z.string().min(1, "Address is required"),
    address_zip: z.string().min(1, "Zip code is required"),
    address_state: z.string().min(1, "State is required"),
    address_city: z.string().min(1, "City is required"),
    date_hired: z.string().min(1, "Hire date is required")
  })
);

type FormValues = {
  firstname: string;
  lastname: string;
  email: string;
  gender: string;
  dob: string;
  mobile: string;
  ssn: string;
  compensation_type: string;
  marital_status: string;
  dependants_count: string;
  address_city: string;
  address_state: string;
  address_full: string;
  address_zip: string;
  date_hired: string;
};

const { resetForm, values, handleSubmit } = useForm<FormValues>({
  validationSchema: schema,
  initialValues: {
    firstname: "",
    lastname: "",
    email: "",
    gender: "",
    dob: "",
    mobile: "",
    ssn: "",
    compensation_type: "",
    marital_status: "",
    dependants_count: "",
    address_city: "",
    address_state: "",
    address_full: "",
    address_zip: "",
    date_hired: "",
  },
});

function toFormValues(e: any): FormValues {
  return {
    firstname: e?.first_name ?? "",
    lastname: e?.last_name ?? "",
    email: e?.party?.email ?? "",
    gender: titleCase(e?.gender),
    dob: e?.dob ?? "",
    mobile: e?.party?.phone_number ?? "",
    ssn: e?.ssn ?? "",
    compensation_type: titleCase(e?.compensation_type),
    marital_status: titleCase(e?.marital_status),
    dependants_count: e?.dependants_count,
    address_city: e?.party?.address_city ?? "",
    address_state: e?.party?.address_state ?? "",
    address_full: e?.party?.address_full ?? "",
    address_zip: e?.party?.address_zip ?? "",
    date_hired: e?.date_hired ?? "",
  };
}

const loading = ref(false);
const error = ref<string | null>(null);
const data = ref<Employee | null>(null);

const emp = computed(() => data.value ?? props.initial ?? null);

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
  () => [props.open, props.employeeId, props.initial] as const,
  async ([open, id, initial]) => {
    if (!open) return;
    const src = initial ?? (id ? await fetchById(id) : null);
    if (src) resetForm({ values: toFormValues(src) });
  },
  { immediate: true }
);

// stub handlers (hook these to your form later)
function onClose() {
  emit("update:open", false);
  emit("cancel");
}



const trimOrUndef = (v: unknown) =>
  typeof v === "string" ? v.trim() || undefined : v;

const addIf = (obj: Record<string, any>, key: string, val: any) => {
  const t = trimOrUndef(val);
  if (t !== undefined && t !== null) obj[key] = t;
};

const lower = (v?: string) => (v ? v.toLowerCase() : v);




const onSave = handleSubmit(async (vals) => {
  if (!props.employeeId && !emp.value?.id) {
    error.value = "Missing employee id for update";
    return;
  }
  loading.value = true; error.value = null;

  try {
    const id = (props.employeeId ?? emp.value?.id)!;
    const baseline = data.value ?? props.initial; // reuse what you already fetched
    const updated = await updateEmployee(id, vals, baseline);

    data.value = updated;
    emit("save", updated);
    emit("update:open", false);
    alert("Employee edited successfully");
  } catch (e: any) {
    const apiMsg = e?.response?.data ?? e?.message ?? "Failed to save changes";
    error.value = typeof apiMsg === "string" ? apiMsg : JSON.stringify(apiMsg);
  } finally {
    loading.value = false;
  }
});



</script>

<template>
  <Dialog :open="open" @update:open="v => emit('update:open', v)">
    <!-- No overflow-hidden + scroll container for zoomed layouts -->
    <DialogContent class="sm:max-w-2xl p-0">
      <div class="max-h-[85vh] overflow-y-auto">
        <div class="p-6">
          <DialogHeader class="p-0 mb-4">
            <DialogTitle>Edit employee</DialogTitle>
            <DialogDescription v-if="emp">
              {{ emp.party?.first_name }} {{ emp.party?.last_name }} • {{ emp.party?.email || "—" }}
            </DialogDescription>
          </DialogHeader>

          <div v-if="loading" class="p-4 text-sm text-muted-foreground">Loading…</div>
          <div v-else-if="error" class="p-4 text-sm text-red-600">{{ error }}</div>

          <Card v-else>
            <!-- Keep content visible so popovers/selects aren’t clipped; form grid lives here -->
            <CardContent class="p-6 overflow-visible">

            <form @submit.prevent= "onSubmit" class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <FormField v-slot="{ componentField }" name="firstname">
                    <FormItem>
                    <FormLabel>First Name</FormLabel>
                    <FormControl>
                        <Input type="text" 
                          v-bind="componentField" 
                          :placeholder="!values.party?.firstname ? 'Enter First Name' : ''"/>
                    </FormControl>
                    <FormMessage />
                    </FormItem>
              </FormField>

              <FormField v-slot="{ componentField }" name="lastname">
                    <FormItem>
                    <FormLabel>Last Name</FormLabel>
                    <FormControl>
                        <Input type="text" 
                          v-bind="componentField" 
                          :placeholder="!values.party?.lastname ? 'Enter Last Name' : ''"/>
                    </FormControl>
                    <FormMessage />
                    </FormItem>
              </FormField>

              <FormField v-slot="{ componentField }" name="dob">
                <FormItem>
                <FormLabel>Date Of Birth</FormLabel>
                <FormControl>
                    <Input
                      type="date"
                      v-bind="componentField"
                      :placeholder="!values.party?.dob ? 'YYYY-MM-DD' : ''"
                    />
                </FormControl>
                </FormItem>
            </FormField>


            <FormField name="gender" v-slot="{ value, handleChange }">
                <FormItem>
                    <FormLabel>Gender</FormLabel>
                    <DropdownMenu>
                    <DropdownMenuTrigger as-child>
                        <FormControl>
                        <Button
                            variant="outline"
                            :class="{
                            'w-full justify-start font-normal': true,
                            'text-muted-foreground': !value,
                            }"
                        >
                            {{ value || 'Select gender' }}
                        </Button>
                        </FormControl>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent>
                        <DropdownMenuItem @click="handleChange('Male')">Male</DropdownMenuItem>
                        <DropdownMenuItem @click="handleChange('Female')">Female</DropdownMenuItem>
                        <DropdownMenuItem @click="handleChange('Other')">Other</DropdownMenuItem>
                    </DropdownMenuContent>
                    </DropdownMenu>
                    <FormMessage />
                </FormItem>
            </FormField>

            <FormField v-slot="{ componentField }" name="mobile">
                <FormItem>
                    <RequiredLabel required>Mobile Number</RequiredLabel>
                    <FormControl>
                    <Input
                        type="tel"
                        :placeholder="!values.party?.mobile ? 'Enter Mobile Number' : ''"
                        v-bind="componentField"
                    />
                    </FormControl>
                    <FormMessage />
                </FormItem>
            </FormField>


            <FormField v-slot="{ componentField }" name="email">
                <FormItem>
                    <RequiredLabel required>Email Address</RequiredLabel>
                    <FormControl>
                    <Input
                        type="email"
                        :placeholder="!values.party?.email ? 'Enter Email Address' : ''"
                        v-bind="componentField"
                    />
                    </FormControl>
                    <FormMessage />
                </FormItem>
            </FormField>


            <FormField v-slot="{ componentField }" name="ssn">
                    <FormItem>
                    <FormLabel>Social Security Number</FormLabel>
                    <FormControl>
                        <Input type="text" 
                          v-bind="componentField" 
                          :placeholder="!values.party?.ssn ? 'XXX-XX-XXXX' : ''"/>
                    </FormControl>
                    <FormMessage />
                    </FormItem>
              </FormField>

              <FormField name="compensation_type" v-slot="{ value, handleChange }">
                <FormItem>
                    <FormLabel>Compensation Type</FormLabel>
                    <DropdownMenu>
                    <DropdownMenuTrigger as-child>
                        <FormControl>
                        <Button
                            variant="outline"
                            :class="{
                            'w-full justify-start font-normal': true,
                            'text-muted-foreground': !value,
                            }"
                        >
                            {{ value || 'Select compensation_type' }}
                        </Button>
                        </FormControl>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent>
                        <DropdownMenuItem @click="handleChange('Salaried')">Salaried</DropdownMenuItem>
                        <DropdownMenuItem @click="handleChange('Hourly')">Hourly</DropdownMenuItem>
                    </DropdownMenuContent>
                    </DropdownMenu>
                    <FormMessage />
                </FormItem>
            </FormField>

            <FormField name="marital_status" v-slot="{ value, handleChange }">
                <FormItem>
                    <FormLabel>Marital Status</FormLabel>
                    <DropdownMenu>
                    <DropdownMenuTrigger as-child>
                        <FormControl>
                        <Button
                            variant="outline"
                            :class="{
                            'w-full justify-start font-normal': true,
                            'text-muted-foreground': !value,
                            }"
                        >
                            {{ value || 'Select marital_status' }}
                        </Button>
                        </FormControl>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent>
                        <DropdownMenuItem @click="handleChange('Single')">Single</DropdownMenuItem>
                        <DropdownMenuItem @click="handleChange('Married')">Married</DropdownMenuItem>
                        <DropdownMenuItem @click="handleChange('Divorced')">Divorced</DropdownMenuItem>
                    </DropdownMenuContent>
                    </DropdownMenu>
                    <FormMessage />
                </FormItem>
            </FormField>


            <FormField name="dependants_count" v-slot="{ value, setValue }">
                <FormItem>
                <FormLabel>Dependants Count</FormLabel>
                <NumberField
                    :model-value="value ?? 0"
                    @update:model-value="v => setValue(Math.min(Math.max(v, 0), 10))"
                >
                    <NumberFieldContent>
                    <NumberFieldDecrement />
                    <FormControl>
                        <NumberFieldInput :min="0" :max="10" />
                    </FormControl>
                    <NumberFieldIncrement />
                    </NumberFieldContent>
                </NumberField>
                <FormMessage />
                </FormItem>
            </FormField>

            <FormField v-slot="{ componentField }" name="address_full">
                <FormItem>
                    <FormLabel>Address</FormLabel>
                    <FormControl>
                        <Input type="text" 
                          :placeholder="!values.party?.address_full ? 'Enter Full Address' : ''"
                          v-bind="componentField" />
                    </FormControl>
                </FormItem>
            </FormField>

            <FormField v-slot="{ componentField }" name="address_city">
                <FormItem>
                    <FormLabel>City</FormLabel>
                    <FormControl>
                        <Input type="text" 
                          :placeholder="!values.party?.address_city ? 'Enter City' : ''"
                          v-bind="componentField" />
                    </FormControl>
                </FormItem>
            </FormField>


            <FormField name="address_state" v-slot="{ value, handleChange }">
                <FormItem>
                    <FormLabel>State</FormLabel>
                    <FormControl>
                    <DropdownMenu>
                        <DropdownMenuTrigger class="w-full border px-4 py-2 rounded-md text-left text-muted-foreground">
                        {{ value || "Select a state" }}
                        </DropdownMenuTrigger>
                        <DropdownMenuContent class="w-full max-h-60 overflow-y-auto">
                        <DropdownMenuItem
                            v-for="state in usStates"
                            :key="state.code"
                            @select="handleChange(state.code)"
                            class="cursor-pointer"
                        >
                            {{ state.name }}
                        </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                    </FormControl>
                    <FormMessage />
                </FormItem>
            </FormField>



            <FormField v-slot="{ componentField }" name="address_zip">
                <FormItem>
                    <FormLabel>Zip Code</FormLabel>
                    <FormControl>
                        <Input type="text" 
                          :placeholder="!values.party?.address_zip ? 'Enter Zip Code' : ''"
                          v-bind="componentField" />
                    </FormControl>
                </FormItem>
            </FormField>

            <FormField v-slot="{ componentField }" name="date_hired">
                <FormItem>
                <FormLabel>Employee Hiring Date</FormLabel>
                <FormControl>
                    <Input type="date" v-bind="componentField" />
                </FormControl>
                </FormItem>
            </FormField>


            </form>

              
            </CardContent>

            <!-- Sticky footer so actions are always visible even when scrolled/zoomed -->
            <CardFooter class="justify-end gap-2 border-t p-4 sticky bottom-0 bg-background">
              <Button variant="ghost" @click="onClose">Close</Button>
              <Button :disabled="loading" @click="onSave">Save changes</Button>
            </CardFooter>
          </Card>
        </div>
      </div>
    </DialogContent>
  </Dialog>
</template>
