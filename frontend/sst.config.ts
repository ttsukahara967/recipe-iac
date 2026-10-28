/// <reference path="./.sst/platform/config.d.ts" />

// Deploys the Next.js frontend to CloudFront + Lambda.
// The backend API URL and the optional custom domain come from Terraform outputs
// via the API_URL / SITE_DOMAIN env vars (see Makefile).
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

    // SST issues the certificate (us-east-1) and creates the DNS records in the Route 53 zone
    const siteDomain = process.env.SITE_DOMAIN;
    // Optional comma-separated hostnames that 301-redirect to the primary site domain.
    // Defaults to redirecting www -> apex in production. Used to temporarily serve an
    // environment on another domain (e.g. develop on the apex, redirecting the develop subdomain).
    const redirectEnv = process.env.SITE_REDIRECTS?.split(",")
      .map((s) => s.trim())
      .filter(Boolean);
    const domain = siteDomain
      ? {
          name: siteDomain,
          redirects: redirectEnv ?? ($app.stage === "production" ? [`www.${siteDomain}`] : undefined),
        }
      : undefined;

    const web = new sst.aws.Nextjs("Web", {
      domain,
      environment: {
        API_URL: apiUrl,
      },
    });

    return { url: web.url };
  },
});
