'use client';

import { useState, useEffect, useMemo } from 'react';
import type { ConfiguredHpcComponent } from '@/lib/types';
import { useDebounce } from '@/hooks/use-debounce';
import { validateYamlConfiguration } from '@/ai/flows/validate-yaml-configuration';
import { useToast } from '@/hooks/use-toast';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { CheckCircle, Download, Loader, XCircle } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Table, TableBody, TableCell, TableFooter, TableHead, TableHeader, TableRow } from '../ui/table';

interface YamlViewerProps {
  configuredComponents: ConfiguredHpcComponent[];
}

function generateYaml(components: ConfiguredHpcComponent[]): string {
  if (components.length === 0) {
    return "# Add components from the catalog to generate the YAML configuration.";
  }

  let yaml = 'apiVersion: hpc.gcp.com/v1alpha1\n';
  yaml += 'kind: HpcCluster\n';
  yaml += 'metadata:\n';
  yaml += '  name: hpc-cluster-example\n';
  yaml += 'spec:\n';
  yaml += '  components:\n';

  components.forEach(comp => {
    yaml += `    - name: ${comp.instanceId}\n`;
    yaml += `      type: ${comp.name.toLowerCase().replace(/ /g, '-')}\n`;
    yaml += `      category: ${comp.category}\n`;
    yaml += '      settings:\n';
    Object.entries(comp.configuredValues).forEach(([key, value]) => {
      yaml += `        ${key}: ${value}\n`;
    });
  });
  return yaml;
}

export function YamlViewer({ configuredComponents }: YamlViewerProps) {
  const { toast } = useToast();
  const [yamlString, setYamlString] = useState('');
  const [validationResult, setValidationResult] = useState<{ isValid: boolean; errors: string[] } | null>(null);
  const [isValidating, setIsValidating] = useState(false);
  
  const debouncedYaml = useDebounce(yamlString, 1000);

  useEffect(() => {
    setYamlString(generateYaml(configuredComponents));
  }, [configuredComponents]);

  useEffect(() => {
    if (!debouncedYaml || debouncedYaml.startsWith('#')) {
      setValidationResult(null);
      return;
    }

    const validate = async () => {
      setIsValidating(true);
      setValidationResult(null);
      try {
        const result = await validateYamlConfiguration({ yamlConfiguration: debouncedYaml });
        setValidationResult(result);
      } catch (error) {
        console.error("Validation failed:", error);
        toast({
          variant: "destructive",
          title: "Validation Error",
          description: "Could not connect to the validation service.",
        });
      } finally {
        setIsValidating(false);
      }
    };
    validate();
  }, [debouncedYaml, toast]);
  
  const costData = useMemo(() => {
    return configuredComponents.map(c => {
        let quantity = 1;
        if(c.category === 'compute' && c.configuredValues.cpuCount) {
             quantity = Number(c.configuredValues.cpuCount);
        }
        if(c.category === 'storage' && c.configuredValues.size) {
            quantity = Number(c.configuredValues.size);
        }
        const total = c.cost * quantity;
        return { name: c.name, quantity, unit: c.costUnit, costPerUnit: c.cost, total };
    });
  }, [configuredComponents]);

  const totalCost = useMemo(() => costData.reduce((sum, item) => sum + item.total, 0), [costData]);


  const handleDownload = () => {
    const blob = new Blob([yamlString], { type: 'application/x-yaml;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'hpc-config.yaml';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const ValidationStatus = () => {
    if (isValidating) {
      return <div className="flex items-center gap-2 text-muted-foreground"><Loader className="animate-spin w-4 h-4" /> <span>Validating...</span></div>;
    }
    if (!validationResult) {
      return <div className="text-muted-foreground">Awaiting input...</div>;
    }
    if (validationResult.isValid) {
      return <div className="flex items-center gap-2 text-primary"><CheckCircle className="w-4 h-4" /> <span>Configuration is valid.</span></div>;
    }
    return <div className="flex items-center gap-2 text-destructive"><XCircle className="w-4 h-4" /> <span>Validation failed.</span></div>;
  };

  return (
    <Tabs defaultValue="yaml" className="w-full h-full flex flex-col">
      <TabsList className="grid w-full grid-cols-3">
        <TabsTrigger value="yaml">YAML</TabsTrigger>
        <TabsTrigger value="validation">
            <div className="flex items-center gap-2">
                <span>Validation</span>
                {isValidating ? <Loader className="animate-spin w-3 h-3"/> : validationResult && (
                    validationResult.isValid ? <CheckCircle className="w-3 h-3 text-primary"/> : <XCircle className="w-3 h-3 text-destructive"/>
                )}
            </div>
        </TabsTrigger>
        <TabsTrigger value="cost">Cost</TabsTrigger>
      </TabsList>
      <TabsContent value="yaml" className="flex-1 flex flex-col overflow-hidden mt-4">
        <ScrollArea className="flex-1 rounded-md border">
            <pre className="text-xs p-4 font-mono"><code >{yamlString}</code></pre>
        </ScrollArea>
        <Button onClick={handleDownload} className="mt-4 w-full" disabled={configuredComponents.length === 0}>
            <Download className="mr-2 h-4 w-4" /> Export YAML
        </Button>
      </TabsContent>
      <TabsContent value="validation" className="flex-1 overflow-y-auto mt-4">
        <div className="p-4 rounded-lg border space-y-4">
            <h3 className="font-semibold"><ValidationStatus/></h3>
            {validationResult && !validationResult.isValid && (
                <div className="space-y-2">
                    <h4 className="font-medium text-sm">Errors:</h4>
                    <ul className="list-disc pl-5 space-y-1">
                        {validationResult.errors.map((error, i) => (
                            <li key={i} className="text-xs text-destructive">{error}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
      </TabsContent>
      <TabsContent value="cost" className="flex-1 overflow-y-auto mt-4">
        <div className="space-y-4">
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>Component</TableHead>
                        <TableHead className="text-right">Total Cost</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {costData.map((item, i) => (
                        <TableRow key={i}>
                            <TableCell>
                                <div className="font-medium">{item.name}</div>
                                <div className="text-xs text-muted-foreground">
                                    {item.quantity.toLocaleString()} x ${item.costPerUnit.toFixed(2)} / {item.unit}
                                </div>
                            </TableCell>
                            <TableCell className="text-right">${item.total.toFixed(2)}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
                <TableFooter>
                    <TableRow>
                        <TableCell className="font-bold text-base">Estimated Total</TableCell>
                        <TableCell className="text-right font-bold text-base text-primary">${totalCost.toFixed(2)} / hr</TableCell>
                    </TableRow>
                </TableFooter>
            </Table>
            <p className="text-xs text-muted-foreground text-center pt-2">
                This is an estimate. Actual costs may vary.
            </p>
        </div>
      </TabsContent>
    </Tabs>
  );
}
