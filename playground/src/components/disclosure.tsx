import * as Collapsible from '@radix-ui/react-collapsible';
import { useState } from "react";
import { twMerge } from 'tailwind-merge'

export default function Disclosure({ title, children, className }: { title: string, children: JSX.Element | JSX.Element[], className?: string }) {
  const [open, setOpen] = useState(false);

  return (
    <Collapsible.Root>
      <Collapsible.Trigger className={twMerge("text-gray-500 font-medium mt-2", className)} onClick={() => setOpen(!open)}>
        <span className="inline-block transform transition-transform duration-200 mr-1" style={{ transform: open ? "rotate(90deg)" : "rotate(0deg)" }}>
          ▶
        </span>
        {title}
      </Collapsible.Trigger>
      <Collapsible.Content className='ml-4'>
        {children}
      </Collapsible.Content>
    </Collapsible.Root>
  );
}