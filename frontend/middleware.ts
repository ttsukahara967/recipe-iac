import { NextRequest, NextResponse } from "next/server";
import { defaultLocale, locales } from "@/i18n/config";

// Redirect any path without a locale prefix to the default locale, e.g. / -> /ja,
// /recipes/x -> /ja/recipes/x. Static assets and Next internals are excluded by the matcher.
export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  const hasLocale = locales.some((locale) => pathname === `/${locale}` || pathname.startsWith(`/${locale}/`));
  if (hasLocale) return NextResponse.next();

  const url = request.nextUrl.clone();
  url.pathname = `/${defaultLocale}${pathname === "/" ? "" : pathname}`;
  return NextResponse.redirect(url);
}

export const config = {
  // Skip Next internals and any path with a file extension (images, etc.)
  matcher: ["/((?!_next/|.*\\..*).*)"],
};
