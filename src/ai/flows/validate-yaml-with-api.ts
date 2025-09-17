'use server';

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const API_BASE_URL = 'http://127.0.0.1:8000';

const ValidateYamlWithApiInputSchema = z.object({
  yaml_content: z.string().describe('The YAML configuration string to validate.'),
  // These are placeholders for now, the UI will need to provide these.
  region: z.string().default('us-central1'),
  zone: z.string().default('us-central1-a'),
});

export type ValidateYamlWithApiInput = z.infer<
  typeof ValidateYamlWithApiInputSchema
>;

const ValidateYamlWithApiOutputSchema = z.object({
  is_valid: z.boolean().describe('Whether the YAML configuration is valid.'),
  errors: z.array(z.string()).describe('A list of validation errors, if any.'),
});

export type ValidateYamlWithApiOutput = z.infer<
  typeof ValidateYamlWithApiOutputSchema
>;

export async function validateYamlWithApi(
  input: ValidateYamlWithApiInput
): Promise<ValidateYamlWithApiOutput> {
  return validateYamlWithApiFlow(input);
}

const validateYamlWithApiFlow = ai.defineFlow(
  {
    name: 'validateYamlWithApiFlow',
    inputSchema: ValidateYamlWithApiInputSchema,
    outputSchema: ValidateYamlWithApiOutputSchema,
  },
  async input => {
    const response = await fetch(`${API_BASE_URL}/validate`, {
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
    return {
      is_valid: result.is_valid,
      errors: result.errors || [],
    };
  }
);
