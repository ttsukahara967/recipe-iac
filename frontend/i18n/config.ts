export const locales = ["ja", "en", "zh-Hant", "zh-Hans", "ko"] as const;
export type Locale = (typeof locales)[number];
export const defaultLocale: Locale = "ja";

export function isLocale(value: string): value is Locale {
  return (locales as readonly string[]).includes(value);
}
