'use client';

import { useState, useEffect, useMemo } from 'react';
import type { ConfiguredHpcComponent } from '@/lib/types';
import { useDebounce } from '@/hooks/use-debounce';
import { validateYamlWithApi, ValidateYamlWithApiOutput } from '@/ai/flows/validate-yaml-with-api';
import { estimateCostWithApi, EstimateCostWithApiOutput } from '@/ai/flows/estimate-cost-with-api';
import { useToast } from '@/hooks/use-toast';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { CheckCircle, Download, Loader, XCircle } from 'lucide-react';
import { Table, TableBody, TableCell, TableFooter, TableHead, TableHeader, TableRow } from '../ui/table';

interface YamlViewerProps {
  configuredComponents: ConfiguredHpcComponent[];
}

function generateYaml(components: ConfiguredHpcComponent[]): string {
  if (components.length === 0) {
    return "# Add components from the catalog to generate the YAML configuration.";
  }

  // --- Start of YAML generation ---
  let blueprintName = "hpc-cluster-example";

  // Base structure
  const blueprint: any = {
    blueprint_name: blueprintName,
    vars: {
      project_id: "your-gcp-project-id", // Fix: Add default project_id
      deployment_name: "hpc-deployment",
      region: "us-central1",
      zone: "us-central1-a",
    },
    deployment_groups: [
      {
        group: "primary",
        modules: [],
      },
    ],
  };

  // Dynamically add modules from configured components
  const modules = components.map(comp => {
    const settings: Record<string, any> = { ...comp.configuredValues };
    const module: Record<string, any> = {
      id: comp.instanceId,
      source: `community/modules/${comp.category}/${comp.id}`, // Example source
      settings: settings,
    };
    return module;
  });

  blueprint.deployment_groups[0].modules = modules;

  // Convert JSON object to YAML string
  // This is a simplified conversion. For complex cases, a library might be better.
  const toYaml = (js: object, indent = 0): string => {
    let yamlString = '';
    const space = '  '.repeat(indent);

    for (const key in js) {
      if (Object.prototype.hasOwnProperty.call(js, key)) {
        const value = (js as any)[key];
        if (Array.isArray(value)) {
          yamlString += `${space}${key}:\n`;
          value.forEach(item => {
            if (typeof item === 'object' && item !== null) {
              const arrayItemStr = toYaml(item, indent + 2);
              yamlString += `${space}  - ${arrayItemStr.trimStart()}\n`;
            } else {
              yamlString += `${space}  - ${item}\n`;
            }
          });
        } else if (typeof value === 'object' && value !== null) {
          yamlString += `${space}${key}:\n`;
          yamlString += toYaml(value, indent + 1);
        } else {
          yamlString += `${space}${key}: ${value}\n`;
        }
      }
    }
    return yamlString;
  };

  return toYaml(blueprint);
}


export function YamlViewer({ configuredComponents }: YamlViewerProps) {
  const { toast } = useToast();
  const [yamlString, setYamlString] = useState('');
  const [validationResult, setValidationResult] = useState<ValidateYamlWithApiOutput | null>(null);
  const [costResult, setCostResult] = useState<EstimateCostWithApiOutput | null>(null);
  const [isValidating, setIsValidating] = useState(false);
  const [isEstimatingCost, setIsEstimatingCost] = useState(false);

  const debouncedYaml = useDebounce(yamlString, 1000);

  useEffect(() => {
    setYamlString(generateYaml(configuredComponents));
  }, [configuredComponents]);

  useEffect(() => {
    if (!debouncedYaml || debouncedYaml.startsWith('#')) {
      setValidationResult(null);
      setCostResult(null);
      return;
    }

    const validate = async () => {
      setIsValidating(true);
      setValidationResult(null);
      try {
        const result = await validateYamlWithApi({ yaml_content: debouncedYaml, region: 'us-central1', zone: 'us-central1-a' });
        setValidationResult({ is_valid: result.is_valid, errors: result.errors });
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

    const estimateCost = async () => {
      setIsEstimatingCost(true);
      setCostResult(null);
      try {
        const result = await estimateCostWithApi({ yaml_content: debouncedYaml, region: 'us-central1', zone: 'us-central1-a' });
        setCostResult(result);
      } catch (error) {
        console.error("Cost estimation failed:", error);
        toast({
          variant: "destructive",
          title: "Cost Estimation Error",
          description: "Could not connect to the cost estimation service.",
        });
      } finally {
        setIsEstimatingCost(false);
      }
    };

    validate();
    estimateCost();
  }, [debouncedYaml, toast]);

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
    if (validationResult.is_valid) {
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
                    validationResult.is_valid ? <CheckCircle className="w-3 h-3 text-primary"/> : <XCircle className="w-3 h-3 text-destructive"/>
                )}
            </div>
        </TabsTrigger>
        <TabsTrigger value="cost">
          <div className="flex items-center gap-2">
            <span>Cost</span>
            {isEstimatingCost ? <Loader className="animate-spin w-3 h-3"/> : costResult && (
              <CheckCircle className="w-3 h-3 text-primary"/>
            )}
          </div>
        </TabsTrigger>
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
            {validationResult && !validationResult.is_valid && (
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
            {isEstimatingCost && <div className="flex items-center justify-center p-8"><Loader className="animate-spin w-8 h-8 text-muted-foreground" /></div>}
            {costResult && (
              <Table>
                  <TableHeader>
                      <TableRow>
                          <TableHead>Component</TableHead>
                          <TableHead className="text-right">Monthly Cost</TableHead>
                      </TableRow>
                  </TableHeader>
                  <TableBody>
                      {Object.entries(costResult.cost_breakdown).map(([key, value]) => (
                        <TableRow key={key}>
                          <TableCell>{key}</TableCell>
                          <TableCell className="text-right">${typeof value === 'number' ? value.toFixed(2) : value}</TableCell>
                        </TableRow>
                      ))}
                  </TableBody>
                  <TableFooter>
                      <TableRow>
                          <TableCell className="font-bold text-base">Estimated Total</TableCell>
                          <TableCell className="text-right font-bold text-base text-primary">${costResult.total_cost.toFixed(2)} / month</TableCell>
                      </TableRow>
                  </TableFooter>
              </Table>
            )}
            <p className="text-xs text-muted-foreground text-center pt-2">
                This is an estimate. Actual costs may vary.
            </p>
        </div>
      </TabsContent>
    </Tabs>
  );
}
