'use client';

import { useState, useCallback } from 'react';
import type { HpcComponent, ConfiguredHpcComponent } from '@/lib/types';
import { AppHeader } from '@/components/hpc/app-header';
import { Catalog } from '@/components/hpc/catalog';
import { Configurator } from '@/components/hpc/configurator';
import { YamlViewer } from '@/components/hpc/yaml-viewer';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';

export default function Home() {
  const [configuredComponents, setConfiguredComponents] = useState<ConfiguredHpcComponent[]>([]);

  const addComponent = useCallback((component: HpcComponent) => {
    const instanceId = `${component.id}-${Date.now()}`;
    const defaultValues = component.configOptions.reduce((acc, option) => {
      acc[option.id] = option.defaultValue;
      return acc;
    }, {} as Record<string, string | number>);

    setConfiguredComponents(prev => [
      ...prev,
      { ...component, instanceId, configuredValues: defaultValues },
    ]);
  }, []);

  const updateComponentConfig = useCallback((instanceId: string, optionId: string, value: string | number) => {
    setConfiguredComponents(prev =>
      prev.map(c =>
        c.instanceId === instanceId
          ? { ...c, configuredValues: { ...c.configuredValues, [optionId]: value } }
          : c
      )
    );
  }, []);

  const removeComponent = useCallback((instanceId: string) => {
    setConfiguredComponents(prev => prev.filter(c => c.instanceId !== instanceId));
  }, []);

  return (
    <div className="flex flex-col h-screen bg-background text-foreground">
      <AppHeader />
      <main className="flex-1 flex flex-col lg:flex-row gap-6 p-6 overflow-hidden">
        <Card className="lg:w-[380px] lg:max-w-[380px] flex flex-col">
          <CardHeader>
            <CardTitle>Component Catalog</CardTitle>
          </CardHeader>
          <ScrollArea className="flex-1">
            <CardContent>
              <Catalog onAddComponent={addComponent} />
            </CardContent>
          </ScrollArea>
        </Card>

        <Card className="flex-1 flex flex-col">
          <CardHeader>
            <CardTitle>Configuration</CardTitle>
          </CardHeader>
          <ScrollArea className="flex-1">
            <CardContent>
              <Configurator
                components={configuredComponents}
                onUpdateConfig={updateComponentConfig}
                onRemoveComponent={removeComponent}
              />
            </CardContent>
          </ScrollArea>
        </Card>

        <Card className="lg:w-[450px] lg:max-w-[450px] flex flex-col">
           <YamlViewer configuredComponents={configuredComponents} />
        </Card>
      </main>
    </div>
  );
}
