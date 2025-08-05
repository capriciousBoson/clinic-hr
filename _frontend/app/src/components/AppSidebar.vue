<script setup lang="ts">
import { Home, LogOut, Users, DollarSign, UserPlus } from "lucide-vue-next"
import {
    Sidebar,
    SidebarContent,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
    SidebarHeader,
    SidebarFooter,
    SidebarMenuSubItem,
    SidebarMenuSub,
    SidebarMenuSubButton
} from "@/components/ui/sidebar"



import type { SidebarProps } from "@/components/ui/sidebar"


const props = defineProps<SidebarProps>()



const data = {
        navMain : [
        {
            title: "Home",
            url: "#",
            icon: Home,
            items: [],
        },
        {
            title: "Employees",
            url: "#",
            icon: Users,
            items: [
            {
                title: "Onboarding",
                url: "#",
                icon: UserPlus,
            },
            ],
        },
        {
            title: "Payroll",
            url: "#",
            icon: DollarSign,
            items: [],
        },
    ]
}


function logout() {
    console.log("Logging out...")
  // add your logout logic here
}

</script>


<template>
    <Sidebar v-bind="props">
        <SidebarHeader>
            <SidebarMenu>
                <SidebarMenuItem>
                    <SidebarMenuButton size="lg" as-child>
                        <a href="#">
                        <div class="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                        <Users class="size-4" />
                        </div>
                        <div class="flex flex-col gap-0.5 leading-none">
                            <span class="font-semibold">Emplyee Management</span>
                            <span class="">v1.0.0</span>
                        </div>
                        </a>
                    </SidebarMenuButton>
                </SidebarMenuItem>
            </SidebarMenu>
        </SidebarHeader>

        <SidebarContent>
        <SidebarGroup>
            <SidebarMenu>
            <SidebarMenuItem v-for="item in data.navMain" :key="item.title">
                <SidebarMenuButton as-child>
                <a :href="item.url" class="font-medium">
                    <component :is="item.icon" class="w-4 h-4" />
                    {{ item.title }}
                </a>
                </SidebarMenuButton>
                <SidebarMenuSub v-if="item.items.length">
                <SidebarMenuSubItem v-for="childItem in item.items" :key="childItem.title">
                    <SidebarMenuSubButton as-child :is-active="childItem.isActive">
                    <a :href="childItem.url">
                        <component :is="childItem.icon" class="w-4 h-4" />
                        {{ childItem.title }}
                    </a>
                    </SidebarMenuSubButton>
                </SidebarMenuSubItem>
                </SidebarMenuSub>
            </SidebarMenuItem>
            </SidebarMenu>
        </SidebarGroup>
    </SidebarContent>

        <SidebarFooter>
            <SidebarMenuItem @click="logout" class="cursor-pointer flex items-center gap-2">
                <span class="icon-wrapper">
                <LogOut class="w-5 h-5" />
                </span>
                <span>Logout</span>
            </SidebarMenuItem>
        </SidebarFooter>
    </Sidebar>
</template>