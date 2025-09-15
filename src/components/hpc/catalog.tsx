'use client';

import { hpcCatalog } from '@/lib/hpc-catalog';
import type { HpcComponent } from '@/lib/types';
import { Button } from '@/components/ui/button';
import { Card, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { PlusCircle } from 'lucide-react';
import React from 'react';

interface CatalogProps {
  onAddComponent: (component: HpcComponent) => void;
}

const ComponentCard = ({ component, onAddComponent }: { component: HpcComponent, onAddComponent: (component: HpcComponent) => void; }) => (
  <Card className="hover:border-primary/50 transition-colors duration-300">
    <CardHeader>
      <div className="flex items-start gap-4">
        <component.icon className="w-8 h-8 text-primary mt-1" />
        <div>
          <CardTitle className="text-lg">{component.name}</CardTitle>
          <CardDescription>{component.description}</CardDescription>
        </div>
      </div>
    </CardHeader>
    <CardFooter>
      <Button variant="outline" className="w-full" onClick={() => onAddComponent(component)}>
        <PlusCircle className="mr-2 h-4 w-4" /> Add to Configuration
      </Button>
    </CardFooter>
  </Card>
);

export function Catalog({ onAddComponent }: CatalogProps) {
  const computeComponents = hpcCatalog.filter(c => c.category === 'compute');
  const storageComponents = hpcCatalog.filter(c => c.category === 'storage');
  const networkComponents = hpcCatalog.filter(c => c.category === 'network');

  return (
    <Tabs defaultValue="compute" className="w-full">
      <TabsList className="grid w-full grid-cols-3">
        <TabsTrigger value="compute">Compute</TabsTrigger>
        <TabsTrigger value="storage">Storage</TabsTrigger>
        <TabsTrigger value="network">Network</TabsTrigger>
      </TabsList>
      <TabsContent value="compute" className="mt-4 space-y-4">
        {computeComponents.map(c => <ComponentCard key={c.id} component={c} onAddComponent={onAddComponent} />)}
      </TabsContent>
      <TabsContent value="storage" className="mt-4 space-y-4">
        {storageComponents.map(c => <ComponentCard key={c.id} component={c} onAddComponent={onAddComponent} />)}
      </TabsContent>
      <TabsContent value="network" className="mt-4 space-y-4">
        {networkComponents.map(c => <ComponentCard key={c.id} component={c} onAddComponent={onAddComponent} />)}
      </TabsContent>
    </Tabs>
  );
}
