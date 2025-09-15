import type { LucideIcon } from 'lucide-react';

export interface ConfigOption {
  id: string;
  label: string;
  type: 'number' | 'select' | 'text' | 'slider';
  defaultValue: string | number;
  options?: { value: string; label: string }[];
  unit?: string;
  description: string;
  min?: number;
  max?: number;
  step?: number;
}

export interface HpcComponent {
  id:string;
  name: string;
  category: 'compute' | 'storage' | 'network';
  description: string;
  cost: number;
  costUnit: string;
  configOptions: ConfigOption[];
  icon: LucideIcon;
}

export type ConfiguredHpcComponent = HpcComponent & {
  instanceId: string;
  configuredValues: Record<string, string | number>;
};
