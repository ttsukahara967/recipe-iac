import "./globals.css";

// Root layout: just the document shell. The visible chrome and the <html lang> live in the
// per-locale layout (app/[locale]/layout.tsx). Locale is a path segment, so the lang here is a
// static default.
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
