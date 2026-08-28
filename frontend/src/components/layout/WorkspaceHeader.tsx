import { Landmark, Search } from 'lucide-react'

import { Button } from '@/components/ui'

import NotificationCenter from '@/components/shared/NotificationCenter'
import { useDemoStore } from '@/store/demoStore'

interface WorkspaceHeaderProps {
  title: string
}

export default function WorkspaceHeader({
  title,
}: Readonly<WorkspaceHeaderProps>) {
  const isDemoMode = useDemoStore((state) => state.isDemoMode)

  const openSearch = () => {
    document.dispatchEvent(new CustomEvent('open-command-palette'))
  }

  return (
    <header className="relative z-20 flex min-h-[calc(3.5rem+env(safe-area-inset-top))] shrink-0 items-center justify-between border-b border-[var(--hairline-2)] bg-[var(--header-bg)] px-3 pt-[env(safe-area-inset-top)] pr-[max(0.75rem,env(safe-area-inset-right))] pl-[max(4rem,env(safe-area-inset-left))] lg:px-4">
      <div className={`flex min-w-0 items-center gap-2.5 ${isDemoMode ? 'invisible sm:visible' : ''}`}>
        <span className="flex size-7 shrink-0 items-center justify-center rounded-md border border-[var(--hairline-2)] bg-[var(--overlay-2)] text-text-secondary">
          <Landmark className="size-3.5" />
        </span>
        <span className="truncate text-sm font-medium text-text-secondary">
          {title}
        </span>
      </div>

      <div className="flex shrink-0 items-center gap-1.5">
        <Button
          type="button"
          variant="secondary"
          size="sm"
          onClick={openSearch}
          className="hidden px-3 text-xs text-muted-foreground hover:text-foreground sm:inline-flex"
          aria-label="Search workspace"
        >
          <Search className="size-3.5" />
          Search
          <kbd className="rounded border border-[var(--hairline-2)] bg-[var(--overlay-2)] px-1 py-0.5 text-[10px] font-medium text-text-tertiary">
            Ctrl K
          </kbd>
        </Button>

        {!isDemoMode && <NotificationCenter />}
      </div>
    </header>
  )
}
