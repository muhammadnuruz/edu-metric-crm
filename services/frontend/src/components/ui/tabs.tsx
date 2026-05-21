"use client"

import * as React from "react"
import * as TabsPrimitive from "@radix-ui/react-tabs"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

function Tabs({ className, ...props }: React.ComponentProps<typeof TabsPrimitive.Root>) {
  return <TabsPrimitive.Root data-slot="tabs" className={cn("flex flex-col gap-2", className)} {...props} />
}

const tabsListVariants = cva("inline-flex w-fit items-center justify-center rounded-lg bg-muted p-1 text-muted-foreground", {
  variants: {
    variant: {
      default: "bg-muted",
      line: "gap-1 bg-transparent",
    },
  },
  defaultVariants: {
    variant: "default",
  },
})

function TabsList({
  className,
  variant,
  ...props
}: React.ComponentProps<typeof TabsPrimitive.List> & VariantProps<typeof tabsListVariants>) {
  return <TabsPrimitive.List data-slot="tabs-list" className={cn(tabsListVariants({ variant }), className)} {...props} />
}

function TabsTrigger({ className, ...props }: React.ComponentProps<typeof TabsPrimitive.Trigger>) {
  return (
    <TabsPrimitive.Trigger
      data-slot="tabs-trigger"
      className={cn("inline-flex items-center justify-center rounded-md px-3 py-1 text-sm font-medium transition-colors data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm", className)}
      {...props}
    />
  )
}

function TabsContent({ className, ...props }: React.ComponentProps<typeof TabsPrimitive.Content>) {
  return <TabsPrimitive.Content data-slot="tabs-content" className={cn("flex-1 text-sm outline-none", className)} {...props} />
}

export { Tabs, TabsList, TabsTrigger, TabsContent, tabsListVariants }
