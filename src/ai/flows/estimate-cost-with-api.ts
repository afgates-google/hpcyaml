'use server';

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const API_BASE_URL = 'http://127.0.0.1:8000';

const EstimateCostWithApiInputSchema = z.object({
  yaml_content: z.string().describe('The YAML configuration string to estimate cost for.'),
  // These are placeholders for now, the UI will need to provide these.
  region: z.string().default('us-central1'),
  zone: z.string().default('us-central1-a'),
});

export type EstimateCostWithApiInput = z.infer<
  typeof EstimateCostWithApiInputSchema
>;

const CostBreakdownSchema = z.object({
    "Compute (CPUs)": z.number(),
    "Compute (RAM)": z.number(),
    "Accelerators (GPUs)": z.number(),
    "Accelerators (TPUs)": z.number(),
    "Storage": z.number(),
});

const EstimateCostWithApiOutputSchema = z.object({
  total_cost: z.number().describe('The total estimated monthly cost.'),
  cost_breakdown: CostBreakdownSchema.describe('A breakdown of the estimated cost.'),
});

export type EstimateCostWithApiOutput = z.infer<
  typeof EstimateCostWithApiOutputSchema
>;

export async function estimateCostWithApi(
  input: EstimateCostWithApiInput
): Promise<EstimateCostWithApiOutput> {
  return estimateCostWithApiFlow(input);
}

const estimateCostWithApiFlow = ai.defineFlow(
  {
    name: 'estimateCostWithApiFlow',
    inputSchema: EstimateCostWithApiInputSchema,
    outputSchema: EstimateCostWithApiOutputSchema,
  },
  async input => {
    const response = await fetch(`${API_BASE_URL}/cost`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(input),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API request failed: ${response.status} ${errorText}`);
    }

    const result = await response.json();
    return result;
  }
);
