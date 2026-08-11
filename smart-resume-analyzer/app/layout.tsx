import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Smart Resume Analyzer & ATS Checker',
  description: 'Explainable AI-assisted resume analysis, ATS scoring, green flags, red flags, and actionable recommendations.'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}
