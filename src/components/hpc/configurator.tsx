'use client';

import type { ConfiguredHpcComponent, ConfigOption } from '@/lib/types';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { Info, Trash2 } from 'lucide-react';
import React from 'react';

interface ConfiguratorProps {
  components: ConfiguredHpcComponent[];
  onUpdateConfig: (instanceId: string, optionId: string, value: string | number) => void;
  onRemoveComponent: (instanceId: string) => void;
}

const ConfigField = ({ instanceId, option, value, onUpdateConfig }: { instanceId: string, option: ConfigOption, value: string | number, onUpdateConfig: ConfiguratorProps['onUpdateConfig'] }) => {
  const renderField = () => {
    switch (option.type) {
      case 'text':
      case 'number':
        return <Input type={option.type} id={option.id} value={value} onChange={(e) => onUpdateConfig(instanceId, option.id, e.target.value)} className="bg-background" />;
      case 'select':
        return (
          <Select value={String(value)} onValueChange={(val) => onUpdateConfig(instanceId, option.id, val)}>
            <SelectTrigger><SelectValue /></SelectTrigger>
            <SelectContent>
              {option.options?.map(opt => <SelectItem key={opt.value} value={opt.value}>{opt.label}</SelectItem>)}
            </SelectContent>
          </Select>
        );
      case 'slider':
        return (
          <div className="flex items-center gap-4">
             <Slider
              value={[Number(value)]}
              onValueChange={([val]) => onUpdateConfig(instanceId, option.id, val)}
              min={option.min}
              max={option.max}
              step={option.step}
            />
            <span className="text-sm font-medium w-24 text-right">{value} {option.unit}</span>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="grid gap-2">
      <div className="flex items-center gap-2">
        <Label htmlFor={option.id}>{option.label}</Label>
        <TooltipProvider>
            <Tooltip>
                <TooltipTrigger asChild>
                    <Info className="w-4 h-4 text-muted-foreground cursor-help" />
                </TooltipTrigger>
                <TooltipContent>
                    <p>{option.description}</p>
                </TooltipContent>
            </Tooltip>
        </TooltipProvider>
      </div>
      {renderField()}
    </div>
  );
};


export function Configurator({ components, onUpdateConfig, onRemoveComponent }: ConfiguratorProps) {
  if (components.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center p-8 border-2 border-dashed border-border rounded-lg h-full">
        <p className="text-muted-foreground">No components selected.</p>
        <p className="text-sm text-muted-foreground/70">Add components from the catalog to begin configuration.</p>
      </div>
    );
  }

  return (
    <Accordion type="multiple" defaultValue={components.map(c => c.instanceId)} className="w-full space-y-4">
      {components.map(component => (
        <AccordionItem key={component.instanceId} value={component.instanceId} className="border-b-0 rounded-lg border bg-card/50 px-4">
          <AccordionTrigger className="hover:no-underline">
            <div className="flex items-center gap-4 w-full">
                <component.icon className="w-6 h-6 text-primary" />
                <span className="font-medium text-lg">{component.name}</span>
                <span className="text-xs text-muted-foreground ml-2 truncate hidden sm:inline">{component.instanceId}</span>
            </div>
          </AccordionTrigger>
          <AccordionContent className="pt-4 space-y-4">
             {component.configOptions.map(option => (
                <ConfigField
                    key={option.id}
                    instanceId={component.instanceId}
                    option={option}
                    value={component.configuredValues[option.id]}
                    onUpdateConfig={onUpdateConfig}
                />
             ))}
             <div className="flex justify-end pt-2">
                <Button variant="destructive" size="sm" onClick={() => onRemoveComponent(component.instanceId)}>
                    <Trash2 className="w-4 h-4 mr-2" />
                    Remove Component
                </Button>
             </div>
          </AccordionContent>
        </AccordionItem>
      ))}
    </Accordion>
  );
}
