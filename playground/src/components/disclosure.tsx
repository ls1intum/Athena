import * as Collapsible from '@radix-ui/react-collapsible';
import { useState } from "react";
import { twMerge } from 'tailwind-merge'

type DisclosureProps = {
  title: string,
  children: JSX.Element | JSX.Element[],
  className?: string,
  openedInitially?: boolean
}

export default function Disclosure({ title, children, className, openedInitially }: DisclosureProps) {
  const [open, setOpen] = useState(openedInitially ?? false);

  return (
    <Collapsible.Root open={open} onOpenChange={setOpen}>
      <Collapsible.Trigger className={twMerge("text-gray-500 font-medium", className)}>
        <span className="inline-block transform transition-transform duration-200 mr-1" style={{ transform: open ? "rotate(90deg)" : "rotate(0deg)" }}>
          ▶
        </span>
        {title}
      </Collapsible.Trigger>
      <Collapsible.Content className='ml-4 mt-1'>
        {children}
      </Collapsible.Content>
    </Collapsible.Root>
  );
}