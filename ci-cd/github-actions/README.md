# How can I use GitHub Actions with Openlayer?

Openlayer for GitHub automatically generates outputs and tests your GitHub projects with Openlayer, providing feedback on the quality of your AI systems with every change you make.

For advanced use cases, you can use Openlayer with GitHub Actions as your CI/CD provider to generate outputs on your datasets for every `git` push. This can then be pushed to Openlayer to run tests under any conditions you’d like.

This approach is useful for developers who want full control over their CI/CD pipeline, as well as GitHub Enterprise Server users, who can’t leverage Openlayer’s built-in git integration. It’s also useful for users whose [execution runtime](https://docs.openlayer.com/development/openlayer-json#model-object-attributes) may not be supported by Openlayer.

## Generating Outputs

You can generate your AI system’s outputs locally (or in GitHub Actions) without giving Openlayer access to the source code through `openlayer batch`. This will generate outputs and expect them to be placed in your model’s `outputDirectory` folder conforming the the [Batch Output specification](https://docs.openlayer.com/development/configuring-output-generation#providing-a-way-for-openlayer-to-run-your-model-on-your-datasets).

`openlayer batch` allows you to generate your AI system’s outputs within your own CI setup, either on GitHub Actions or your own CI, and upload *only* the artifacts (and not the source code) to Openlayer to create a new project version.

## Configuring GitHub Actions for Openlayer

`openlayer push` will upload the artifacts in your working directory (skipping everything in `.openlayerignore`) to Openlayer. Openlayer will auto detect that your outputs have already been created and go straight to computing your metrics and running your tests.

Let’s create our Action with a new file called `.github/workflows/openlayer.yaml`

```yaml
name: Openlayer Tests
env:
  OPENLAYER_PROJECT_ID: ${{ secrets.OPENLAYER_PROJECT_ID }}
  # Anything else you need for your AI to generate outputs
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
on:
  push:
    branches:
      - main
jobs:
  Test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install Openlayer CLI
        run: curl -o- "https://downloads.openlayer.com/cli/install/linux_arm64.sh" | sh
      - name: Install Your Requirements
        run: openlayer install
      - name: Generate Outputs
        run: openlayer batch --api-key=${{ secrets.OPENLAYER_API_KEY }}
      - name: Push Project Artifacts to Openlayer
        run: openlayer push --message ${{ github.event.head_commit.message }} --api-key=${{ secrets.OPENLAYER_API_KEY }}
```

This Action will run when your code is pushed to a git branch. `openlayer push` will wait for the results and cause the Action to fail if any of your tests failed.

Let’s add the required values from Openlayer as secrets in GitHub

1. Retrieve your [Openlayer API key](https://docs.openlayer.com/workspace-and-projects/find-your-api-key)
2. Install the Openlayer CLI and run `openlayer login`
3. Inside your folder, run `openlayer link` to create a new Openlayer project
4. Inside the generated `.openlayer` folder, save the `projectId from the config.json`
5. Inside GitHub, add `OPENLAYER_API_KEY`, `OPENLAYER_PROJECT_ID` and `OPENAI_API_KEY` as [secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)

## Testing Openlayer + Your AI with GitHub Actions

Now that your Openlayer AI system is configured with GitHub Actions, you can try out the workflow:

- Create a new pull request in your GitHub repository
- Merge the pull request into your main branch
- GitHub Actions will recognize the change and use the Openlayer CLI to push your AI
- The Action passes or fails based on the results of your tests

Every merge into your branch of choice will now be tested with Openlayer.
