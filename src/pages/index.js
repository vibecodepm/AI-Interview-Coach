
import OnboardingPage from '../components/OnboardingPage';
import Head from 'next/head';

// This component serves as the functional entry point for our Next.js application.
export default function Home() {
    return (
        <div className="min-h-screen bg-gray-50">
            <Head>
                <title>AI Interview Coach MVP</title>
                <meta name="description" content="AI-powered mock interview platform for PM/Product roles." />
            </Head>

            {/* Main container displaying the core onboarding component */}
            <main className="pt-10 pb-20 bg-gray-50 min-h-screen">
                <OnboardingPage />
            </main>
        </div>
    );
}