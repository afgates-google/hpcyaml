import type { HpcComponent } from './types';
import { Cpu, HardDrive, Network, Server, Database } from 'lucide-react';

export const hpcCatalog: HpcComponent[] = [
  {
    id: 'c2-standard-8',
    name: 'C2 Standard 8',
    category: 'compute',
    description: 'General-purpose machine with a balance of price and performance.',
    cost: 0.33,
    costUnit: 'vCPU/hr',
    icon: Cpu,
    configOptions: [
      {
        id: 'cpuCount',
        label: 'vCPUs',
        type: 'slider',
        defaultValue: 8,
        min: 2,
        max: 60,
        step: 2,
        description: 'Number of virtual CPUs.'
      },
      {
        id: 'memory',
        label: 'Memory',
        type: 'slider',
        defaultValue: 32,
        unit: 'GB',
        min: 8,
        max: 240,
        step: 4,
        description: 'Amount of RAM.'
      },
      {
        id: 'os',
        label: 'Operating System',
        type: 'select',
        defaultValue: 'debian-11',
        options: [
          { value: 'debian-11', label: 'Debian 11' },
          { value: 'ubuntu-2204', label: 'Ubuntu 22.04 LTS' },
          { value: 'centos-stream-9', label: 'CentOS Stream 9' }
        ],
        description: 'The base operating system for the instance.'
      }
    ]
  },
  {
    id: 'a2-highgpu-1g',
    name: 'A2 High-GPU 1G',
    category: 'compute',
    description: 'Optimized for ML/AI with NVIDIA A100 GPUs.',
    cost: 3.75,
    costUnit: 'GPU/hr',
    icon: Server,
    configOptions: [
      {
        id: 'gpuCount',
        label: 'A100 GPUs',
        type: 'select',
        defaultValue: '1',
        options: [
            { value: '1', label: '1 GPU' },
            { value: '2', label: '2 GPUs' },
            { value: '4', label: '4 GPUs' },
            { value: '8', label: '8 GPUs' },
            { value: '16', label: '16 GPUs' }
        ],
        description: 'Number of NVIDIA A100 GPUs.'
      },
       {
        id: 'cpuCount',
        label: 'vCPUs',
        type: 'select',
        defaultValue: '12',
        options: [
            { value: '12', label: '12 vCPUs' },
            { value: '24', label: '24 vCPUs' },
            { value: '48', label: '48 vCPUs' },
            { value: '96', label: '96 vCPUs' },
        ],
        description: 'Number of virtual CPUs.'
      },
      {
        id: 'memory',
        label: 'Memory',
        type: 'select',
        defaultValue: '85',
        unit: 'GB',
        options: [
            { value: '85', label: '85 GB' },
            { value: '170', label: '170 GB' },
            { value: '340', label: '340 GB' },
            { value: '680', label: '680 GB' },
        ],
        description: 'Amount of RAM.'
      }
    ]
  },
  {
    id: 'persistent-ssd',
    name: 'Persistent SSD',
    category: 'storage',
    description: 'High-performance block storage.',
    cost: 0.17,
    costUnit: 'GB/mo',
    icon: HardDrive,
    configOptions: [
      {
        id: 'size',
        label: 'Disk Size',
        type: 'slider',
        defaultValue: 500,
        unit: 'GB',
        min: 10,
        max: 65536,
        step: 10,
        description: 'Size of the persistent disk.'
      },
      {
        id: 'readIOPS',
        label: 'Read IOPS',
        type: 'number',
        defaultValue: 15000,
        description: 'Maximum read operations per second.'
      },
       {
        id: 'writeIOPS',
        label: 'Write IOPS',
        type: 'number',
        defaultValue: 15000,
        description: 'Maximum write operations per second.'
      }
    ]
  },
  {
    id: 'hyperdisk-balanced',
    name: 'Hyperdisk Balanced',
    category: 'storage',
    description: 'Cost-effective, high-performance block storage.',
    cost: 0.10,
    costUnit: 'GB/mo',
    icon: Database,
    configOptions: [
      {
        id: 'size',
        label: 'Disk Size',
        type: 'slider',
        defaultValue: 1024,
        unit: 'GB',
        min: 10,
        max: 65536,
        step: 10,
        description: 'Size of the Hyperdisk.'
      },
      {
        id: 'iops',
        label: 'IOPS',
        type: 'slider',
        defaultValue: 5000,
        min: 1000,
        max: 160000,
        step: 1000,
        description: 'Provisioned IOPS.'
      },
      {
        id: 'throughput',
        label: 'Throughput',
        type: 'slider',
        defaultValue: 250,
        unit: 'MB/s',
        min: 140,
        max: 2400,
        step: 10,
        description: 'Provisioned throughput.'
      }
    ]
  },
  {
    id: 'vpc-network',
    name: 'VPC Network',
    category: 'network',
    description: 'Virtual Private Cloud for secure networking.',
    cost: 0.01,
    costUnit: 'GB egress',
    icon: Network,
    configOptions: [
      {
        id: 'name',
        label: 'Network Name',
        type: 'text',
        defaultValue: 'hpc-network',
        description: 'Name for the VPC network.'
      },
      {
        id: 'routingMode',
        label: 'Routing Mode',
        type: 'select',
        defaultValue: 'REGIONAL',
        options: [
          { value: 'REGIONAL', label: 'Regional' },
          { value: 'GLOBAL', label: 'Global' }
        ],
        description: 'Dynamic routing mode for the VPC.'
      },
       {
        id: 'mtu',
        label: 'MTU',
        type: 'number',
        defaultValue: 1460,
        description: 'Maximum transmission unit for the network.'
      }
    ]
  }
];
