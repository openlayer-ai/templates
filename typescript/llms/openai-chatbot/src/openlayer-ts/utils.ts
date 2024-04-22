// Define shared interfaces and utilities here
export interface RunReturn {
    output: any;
    otherFields: { [key: string]: any };
}

// Define an interface for the configuration object
export interface Config {
    outputColumnName: string;
    inputVariableNames?: string[];
    metadata: {
        output_timestamp: number;
    };
}
