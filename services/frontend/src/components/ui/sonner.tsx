"use client"

type ToasterProps = {
  className?: string
}

const Toaster = ({ className }: ToasterProps) => {
  return <div data-slot="toaster" className={className} />
}

export { Toaster }
