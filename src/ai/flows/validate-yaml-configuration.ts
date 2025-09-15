'use server';

/**
 * @fileOverview YAML configuration validation flow.
 *
 * - validateYamlConfiguration - A function that validates a YAML configuration string.
 * - ValidateYamlConfigurationInput - The input type for the validateYamlConfiguration function.
 * - ValidateYamlConfigurationOutput - The return type for the validateYamlConfiguration function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const ValidateYamlConfigurationInputSchema = z.object({
  yamlConfiguration: z
    .string()
    .describe('The YAML configuration string to validate.'),
});

export type ValidateYamlConfigurationInput = z.infer<
  typeof ValidateYamlConfigurationInputSchema
>;

const ValidateYamlConfigurationOutputSchema = z.object({
  isValid: z.boolean().describe('Whether the YAML configuration is valid.'),
  errors: z.array(z.string()).describe('A list of validation errors, if any.'),
});

export type ValidateYamlConfigurationOutput = z.infer<
  typeof ValidateYamlConfigurationOutputSchema
>;

export async function validateYamlConfiguration(
  input: ValidateYamlConfigurationInput
): Promise<ValidateYamlConfigurationOutput> {
  return validateYamlConfigurationFlow(input);
}

const validateYamlConfigurationPrompt = ai.definePrompt({
  name: 'validateYamlConfigurationPrompt',
  input: {schema: ValidateYamlConfigurationInputSchema},
  output: {schema: ValidateYamlConfigurationOutputSchema},
  prompt: `You are an expert HPC configuration validator.  You will be given a YAML configuration, and your job is to determine if the configuration is valid and follows HPC deployment standards.

  If the configuration is invalid, return a list of errors in the errors field.
  If the configuration is valid, return an empty list of errors.

  YAML Configuration:
  {{yamlConfiguration}}`,
});

const validateYamlConfigurationFlow = ai.defineFlow(
  {
    name: 'validateYamlConfigurationFlow',
    inputSchema: ValidateYamlConfigurationInputSchema,
    outputSchema: ValidateYamlConfigurationOutputSchema,
  },
  async input => {
    const {output} = await validateYamlConfigurationPrompt(input);
    return output!;
  }
);
