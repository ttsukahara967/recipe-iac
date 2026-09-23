/// <reference path="./.sst/platform/config.d.ts" />

// Deploys the Next.js frontend to CloudFront + Lambda.
// The backend API URL comes from the Terraform output via the API_URL env var (see Makefile).
export default $config({
  app(input) {
    return {
      name: "recipe-iac-frontend",
      home: "aws",
      // Let `sst remove` delete every resource in any stage
      removal: "remove",
      protect: false,
      providers: {
        aws: { region: "ap-northeast-1" },
      },
    };
  },
  async run() {
    const apiUrl = process.env.API_URL;
    if (!apiUrl) {
      throw new Error("API_URL is not set. Run via `make deploy ENV=<env>`.");
    }

    const web = new sst.aws.Nextjs("Web", {
      environment: {
        API_URL: apiUrl,
      },
    });

    return { url: web.url };
  },
});
