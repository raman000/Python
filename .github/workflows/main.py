name: CodeGuru Security Example
on:
  push:
    branches:
      - 'main'

permissions:
  id-token: write
  # for writing security events.
  security-events: write
  # only required for workflows in private repositories
  actions: read
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Respository
        uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Configure aws credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: arn:aws:iam::834121473222:role/CodeGuruSecurityGitHubAccessRole
          aws-region: eu-north-1
          role-session-name: GitHubActionScript

      - name: CodeGuru Security
        uses: aws-actions/codeguru-security@v1
        with:
          source_path: .
          aws_region: eu-north-1
          fail_on_severity: Critical
      - name: Print findings
        run: |
          ls -l
          cat codeguru-security-results.sarif.json

      # If you want content in security scanning, you’ll need to enable codescanning by going into github.
      # https://docs.github.com/en/code-security/code-scanning/automatically-scanning-your-code-for-vulnerabilities-and-errors/configuring-code-scanning-for-a-repository
      - name: Upload result
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: codeguru-security-results.sarif.json
