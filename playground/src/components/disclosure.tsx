import * as Collapsible from '@radix-ui/react-collapsible';
import { useState } from "react";
import { twMerge } from 'tailwind-merge'

type DisclosureProps = {
  title: string,
  children: string | JSX.Element | JSX.Element[],
  classNameTrigger?: string,
  className?: string,
  openedInitially?: boolean,
  noContentIndent?: boolean,
}

export default function Disclosure({ title, children, classNameTrigger, className, openedInitially, noContentIndent }: DisclosureProps) {
  const [open, setOpen] = useState(openedInitially ?? false);

  return (
    <Collapsible.Root open={open} onOpenChange={setOpen}>
      <Collapsible.Trigger className={twMerge("text-gray-500 font-medium", classNameTrigger)}>
        <span className="inline-block transform transition-transform duration-200 mr-1" style={{ transform: open ? "rotate(90deg)" : "rotate(0deg)" }}>
          ▶
        </span>
        {title}
      </Collapsible.Trigger>
      <Collapsible.Content className={twMerge('mt-1', noContentIndent ? '' : 'ml-4', className)}>
        {children}
      </Collapsible.Content>
    </Collapsible.Root>
  );
}