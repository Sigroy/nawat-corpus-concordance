import { BookOpen, Library, Search, Settings2 } from "lucide-react";
import Link from "next/link";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";
const ADMIN_URL = API_BASE.replace(/\/api\/?$/, "/admin/");

const navItems = [
  { href: "/concordance", label: "Concordance", icon: Search },
  { href: "/dictionary", label: "Dictionary", icon: BookOpen },
  { href: "/sources", label: "Sources", icon: Library }
];

export function AppNav() {
  return (
    <header className="border-b border-line bg-bone/90">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3 sm:px-6">
        <Link href="/" className="flex min-w-0 items-center gap-3">
          <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md border border-ink bg-ink text-sm font-semibold text-bone">
            NC
          </span>
          <span className="min-w-0">
            <span className="block truncate text-base font-semibold tracking-normal text-ink">
              Nawat Corpus Concordance
            </span>
            <span className="block truncate text-xs text-moss">Concordance Nawat</span>
          </span>
        </Link>
        <nav className="hidden items-center gap-1 md:flex">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="inline-flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium text-ink hover:bg-paper"
            >
              <item.icon className="h-4 w-4" aria-hidden="true" />
              {item.label}
            </Link>
          ))}
        </nav>
        <a
          href={ADMIN_URL}
          className="inline-flex h-10 w-10 items-center justify-center rounded-md border border-line bg-bone text-ink shadow-sm hover:border-teal"
          title="Admin"
        >
          <Settings2 className="h-4 w-4" aria-hidden="true" />
        </a>
      </div>
    </header>
  );
}
