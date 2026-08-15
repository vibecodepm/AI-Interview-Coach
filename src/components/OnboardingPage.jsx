import React, { useMemo, useState } from 'react';
import { startInterview, submitAnswer } from '../services/interviewService';

const EMPTY_EVALUATION = null;

export default function OnboardingPage() {
  const [resumeContent, setResumeContent] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [targetRole, setTargetRole] = useState('AI Product Manager');

  const [stage, setStage] = useState('setup'); // setup | interview | complete
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [evaluation, setEvaluation] = useState(EMPTY_EVALUATION);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const currentQuestion = questions[currentIndex];

  const canStart = useMemo(
    () =>
      resumeContent.trim().length >= 10 &&
      jobDescription.trim().length >= 10 &&
      targetRole.trim().length > 0 &&
      !loading,
    [resumeContent, jobDescription, targetRole, loading]
  );

  const canSubmit =
  answer.trim().length >= 5 &&
  !loading &&
  !evaluation;

  async function handleStartInterview() {
    if (!canStart) return;

    setLoading(true);
    setError('');

    try {
      const data = await startInterview({
        resume_text: resumeContent,
        job_description: jobDescription,
        target_role: targetRole,
      });

      setQuestions(Array.isArray(data) ? data : []);
      setCurrentIndex(0);
      setAnswer('');
      setEvaluation(null);
      setResults([]);
      setStage('interview');
    } catch (err) {
      setError(err.message || 'Unable to start the interview.');
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmitAnswer() {
    if (!currentQuestion || !canSubmit || evaluation) return;

    setLoading(true);
    setError('');

    try {
      const data = await submitAnswer({
        question_id: currentQuestion.question_id,
        question_text:
          currentQuestion.question_text ||
          currentQuestion.rawText ||
          currentQuestion.title,
        suggested_framework: currentQuestion.suggested_framework,
        user_answer: answer,
        target_role: targetRole,
      });

      setEvaluation(data);

setResults((previous) => {
  const result = {
    question: currentQuestion,
    answer,
    evaluation: data,
    questionIndex: currentIndex,
  };

  const existingIndex = previous.findIndex(
    (item) => item.questionIndex === currentIndex
  );

  if (existingIndex !== -1) {
    const updated = [...previous];
    updated[existingIndex] = result;
    return updated;
  }

  return [...previous, result];
});
    } catch (err) {
      setError(err.message || 'Unable to evaluate the answer.');
    } finally {
      setLoading(false);
    }
  }

  function handleNextQuestion() {
  if (!evaluation) return;

  if (currentIndex >= questions.length - 1) {
    setStage('complete');
    return;
  }

  setCurrentIndex((index) => index + 1);
  setAnswer('');
  setEvaluation(null);
  setError('');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

  function handleRestart() {
    setStage('setup');
    setQuestions([]);
    setCurrentIndex(0);
    setAnswer('');
    setEvaluation(null);
    setResults([]);
    setError('');
  }

  if (stage === 'complete') {
    const overall =
      results.length > 0
        ? (
            results.reduce(
              (sum, item) => sum + Number(item.evaluation.overall_score || 0),
              0
            ) / results.length
          ).toFixed(1)
        : '0.0';

    const dimensionAverages = ['Relevance', 'Structure', 'Specificity', 'Business Impact']
      .map((dimension) => {
        const values = results
          .map((item) =>
            item.evaluation.detailed_scores?.find(
              (score) => score.dimension === dimension
            )?.score_per_dimension
          )
          .filter((value) => typeof value === 'number');

        if (!values.length) return null;

        return {
          dimension,
          score: (values.reduce((a, b) => a + b, 0) / values.length).toFixed(1),
        };
      })
      .filter(Boolean);

    return (
      <main className="min-h-screen bg-slate-50 px-5 py-10">
        <div className="mx-auto max-w-4xl">
          <div className="mb-8">
            <p className="text-sm font-bold uppercase tracking-[0.2em] text-indigo-600">
              Interview complete
            </p>
            <h1 className="mt-2 text-4xl font-extrabold tracking-tight text-slate-900">
              Your Interview Readiness
            </h1>
            <p className="mt-2 text-lg text-slate-600">
              A concise view of how you performed across the mock interview.
            </p>
          </div>

          <section className="rounded-2xl border border-indigo-100 bg-white p-8 shadow-sm">
            <div className="flex flex-col gap-8 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <p className="text-sm font-semibold text-slate-500">Overall score</p>
                <p className="mt-1 text-6xl font-extrabold text-indigo-600">
                  {overall}<span className="text-2xl text-slate-400">/5</span>
                </p>
              </div>
              <div className="text-sm text-slate-500">
                {results.length} of {questions.length} questions completed
              </div>
            </div>

            <div className="mt-8 grid gap-4 sm:grid-cols-2">
              {dimensionAverages.map((item) => (
                <div
                  key={item.dimension}
                  className="rounded-xl border border-slate-200 bg-slate-50 p-5"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-slate-800">{item.dimension}</span>
                    <span className="font-extrabold text-indigo-600">
                      {item.score}/5
                    </span>
                  </div>
                </div>
              ))}
            </div>

            <button
              onClick={handleRestart}
              className="mt-8 w-full rounded-xl bg-gradient-to-r from-indigo-600 to-blue-600 px-6 py-4 text-lg font-bold text-white shadow-lg transition hover:shadow-xl"
            >
              Start Another Mock Interview
            </button>
          </section>
        </div>
      </main>
    );
  }

  if (stage === 'interview' && currentQuestion) {
    const questionText =
      currentQuestion.question_text ||
      currentQuestion.rawText ||
      currentQuestion.title ||
      '';

    const followUps = currentQuestion.follow_up_prompt || [];

    return (
      <main className="min-h-screen bg-slate-50 px-5 py-8">
        <div className="mx-auto max-w-4xl">
          <header className="mb-6 flex items-end justify-between gap-4">
            <div>
              <p className="text-sm font-bold uppercase tracking-[0.2em] text-indigo-600">
                Your interview
              </p>
              <h1 className="mt-1 text-3xl font-extrabold text-slate-900">
                Question {currentIndex + 1} of {questions.length}
              </h1>
              <p className="mt-1 text-slate-500">
                Answer as you would in a real interview. Be specific and quantify
                your impact where possible.
              </p>
            </div>
            <div className="rounded-full bg-white px-4 py-2 text-sm font-bold text-slate-700 shadow-sm">
              {currentIndex + 1}/{questions.length}
            </div>
          </header>

          <section className="rounded-2xl border border-indigo-100 bg-white p-8 shadow-sm">
            <p className="text-sm font-bold uppercase tracking-[0.15em] text-indigo-600">
              ● Interview question
            </p>

            <h2 className="mt-4 text-2xl font-extrabold leading-tight text-slate-900 sm:text-3xl">
              {questionText}
            </h2>

            {currentQuestion.suggested_framework && (
              <div className="mt-6 rounded-xl border-l-4 border-indigo-500 bg-indigo-50 p-5">
                <p className="text-sm font-bold text-indigo-700">
                  Required Framework
                </p>
                <p className="mt-2 text-lg font-bold text-indigo-700">
                  {currentQuestion.suggested_framework}
                </p>
                <p className="mt-1 text-sm text-indigo-600">
                  Use this structure to make your answer clear and rigorous.
                </p>
              </div>
            )}

            {followUps.length > 0 && (
              <div className="mt-7">
                <h3 className="text-base font-bold text-slate-800">
                  🔍 Areas the interviewer may probe
                </h3>
                <div className="mt-3 space-y-2">
                  {followUps.map((item, index) => (
                    <div
                      key={`${item}-${index}`}
                      className="rounded-lg border-l-2 border-amber-400 bg-slate-50 px-4 py-3 text-sm text-slate-700"
                    >
                      <span className="mr-2 font-bold text-amber-700">
                        [{index + 1}]
                      </span>
                      {item}
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="mt-7">
              <div className="mb-2 flex items-center justify-between">
                <label className="font-bold text-slate-800" htmlFor="answer">
                  Your Answer
                </label>
                <span className="text-sm text-slate-400">
                  {answer.length} characters
                </span>
              </div>

              <textarea
                id="answer"
                value={answer}
                onChange={(event) => setAnswer(event.target.value)}
                rows={9}
                placeholder="Structure your answer clearly. Explain the context, what you personally did, why you made the decision, and the result."
                className="w-full resize-y rounded-xl border border-slate-300 p-4 text-base text-slate-800 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
              />

              <button
                onClick={handleSubmitAnswer}
                disabled={!canSubmit}
                className="mt-4 w-full rounded-xl bg-gradient-to-r from-indigo-600 to-blue-600 px-6 py-4 font-bold text-white shadow-lg transition hover:shadow-xl disabled:cursor-not-allowed disabled:bg-slate-300 disabled:bg-none disabled:text-slate-500 disabled:shadow-none"
              >
                {loading ? 'Evaluating…' : 'Submit Answer'}
              </button>
            </div>

            {error && (
              <div className="mt-5 rounded-xl border border-red-200 bg-red-50 p-4 text-sm font-medium text-red-700">
                {error}
              </div>
            )}

            {evaluation && (
              <div className="mt-8 border-t border-slate-200 pt-7">
                <div className="rounded-xl bg-slate-50 p-5">
                  <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                    <div>
                      <p className="text-sm font-semibold text-slate-500">
                        AI Evaluation
                      </p>
                      <p className="mt-1 text-4xl font-extrabold text-indigo-600">
                        {Number(evaluation.overall_score).toFixed(1)}
                        <span className="text-lg text-slate-400">/5</span>
                      </p>
                    </div>
                    <p className="max-w-md text-sm text-slate-600">
                      Your answer has been evaluated against the interview rubric.
                      Review the evidence before moving on.
                    </p>
                  </div>

                  <div className="mt-5 grid gap-3 sm:grid-cols-2">
                    {(evaluation.detailed_scores || []).map((score) => (
                      <div
                        key={score.dimension}
                        className="rounded-xl border border-slate-200 bg-white p-4"
                      >
                        <div className="flex items-center justify-between gap-3">
                          <span className="font-bold text-slate-800">
                            {score.dimension}
                          </span>
                          <span className="font-extrabold text-indigo-600">
                            {Number(score.score_per_dimension).toFixed(1)}/5
                          </span>
                        </div>
                        <p className="mt-2 text-sm leading-6 text-slate-600">
                          {score.justification}
                        </p>
                      </div>
                    ))}
                  </div>

                  {evaluation.feedback?.improvements?.length > 0 && (
                    <div className="mt-4 rounded-xl border border-amber-100 bg-amber-50 p-4">
                      <p className="font-bold text-amber-900">
                        Improve next time
                      </p>
                      <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-amber-800">
                        {evaluation.feedback.improvements.map((item) => (
                          <li key={item}>{item}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                <button
                  onClick={handleNextQuestion}
                  className="mt-6 w-full rounded-xl bg-slate-900 px-6 py-4 font-bold text-white shadow-lg transition hover:bg-slate-800"
                >
                  {currentIndex === questions.length - 1
                    ? 'View Interview Summary →'
                    : 'Next Question →'}
                </button>
              </div>
            )}
          </section>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-50 px-5 py-8">
      <div className="mx-auto max-w-4xl">
        <header className="mb-8">
          <p className="text-sm font-bold uppercase tracking-[0.2em] text-indigo-600">
            AI Interview Coach
          </p>
          <h1 className="mt-2 text-4xl font-extrabold tracking-tight text-slate-900 sm:text-5xl">
            Interview Performance <span className="text-indigo-600">Engine.</span>
          </h1>
          <p className="mt-3 max-w-2xl text-lg leading-7 text-slate-600">
            Practice a structured interview, answer one question at a time, and
            receive evidence-based scoring instead of subjective feedback.
          </p>
        </header>

        <section className="mb-8 grid gap-4 sm:grid-cols-3">
          {[
            ['🎯', 'Metrics-Driven Scoring', 'Four explicit dimensions from 0–5.'],
            ['⚡', 'Immediate Feedback', 'See what worked and what to improve.'],
            ['📋', 'Context Grounding', 'Questions are generated from your role context.'],
          ].map(([icon, title, description]) => (
            <div
              key={title}
              className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"
            >
              <div className="text-2xl">{icon}</div>
              <h2 className="mt-3 font-bold text-slate-900">{title}</h2>
              <p className="mt-1 text-sm leading-5 text-slate-500">{description}</p>
            </div>
          ))}
        </section>

        <section className="rounded-2xl border border-slate-200 bg-white p-7 shadow-sm">
          <h2 className="text-2xl font-extrabold text-slate-900">
            Preparation Inputs
          </h2>

          <div className="mt-6 grid gap-5">
            <div>
              <label
                className="mb-2 block font-bold text-slate-800"
                htmlFor="resume"
              >
                1. Professional History
              </label>
              <textarea
                id="resume"
                value={resumeContent}
                onChange={(event) => setResumeContent(event.target.value)}
                rows={5}
                placeholder="Paste your resume text here."
                className="w-full rounded-xl border border-slate-300 p-4 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
              />
            </div>

            <div>
              <label
                className="mb-2 block font-bold text-slate-800"
                htmlFor="jd"
              >
                2. Target Job Description
              </label>
              <textarea
                id="jd"
                value={jobDescription}
                onChange={(event) => setJobDescription(event.target.value)}
                rows={5}
                placeholder="Paste the target job description here."
                className="w-full rounded-xl border border-slate-300 p-4 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
              />
            </div>

            <div>
              <label
                className="mb-2 block font-bold text-slate-800"
                htmlFor="role"
              >
                3. Target Persona
              </label>
              <select
                id="role"
                value={targetRole}
                onChange={(event) => setTargetRole(event.target.value)}
                className="w-full rounded-xl border border-slate-300 bg-white p-4 outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
              >
                <option>AI Product Manager</option>
                <option>Senior Product Manager</option>
                <option>Product Manager</option>
                <option>Product Lead</option>
              </select>
            </div>
          </div>

          {error && (
            <div className="mt-5 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
              {error}
            </div>
          )}

          <button
            onClick={handleStartInterview}
            disabled={!canStart}
            className="mt-6 w-full rounded-xl bg-gradient-to-r from-indigo-600 to-blue-600 px-6 py-4 text-lg font-extrabold text-white shadow-lg transition hover:shadow-xl disabled:cursor-not-allowed disabled:bg-slate-300 disabled:bg-none disabled:text-slate-500 disabled:shadow-none"
          >
            {loading ? 'Preparing Interview…' : 'Start Mock Interview'}
          </button>

          {!canStart && (
            <p className="mt-3 text-center text-sm text-slate-400">
              Add your resume and target job description to begin.
            </p>
          )}
        </section>
      </div>
    </main>
  );
}