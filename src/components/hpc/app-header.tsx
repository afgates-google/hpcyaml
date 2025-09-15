import { Atom } from 'lucide-react';

export function AppHeader() {
  return (
    <header className="p-4 border-b border-border flex items-center gap-3 shrink-0">
      <Atom className="text-primary w-8 h-8" />
      <h1 className="text-2xl font-bold text-foreground">HPC Yamlify</h1>
    </header>
  );
}
