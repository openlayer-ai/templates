// src/run.ts
import CLIHandler from "openlayer/lib/core/cli";
import { MyModel } from "./models/myModel";

// User implements their model
const model = new MyModel();

// Initialize CLI handler with the user's model run method
const cliHandler = new CLIHandler(model.run.bind(model));

// Setup CLI and process dataset
cliHandler.runFromCLI();
