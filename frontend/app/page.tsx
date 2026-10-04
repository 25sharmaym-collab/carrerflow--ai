"use client";

import { FormEvent, useState } from "react";

type Result = {
  match_score: number;
  matched_skills: string[];
  missing_skills: string[];
  suggestions: string[];
  preferred_matches: string[];
  ats_score: number;
  ats_warnings: string[];
  interview_questions: string[];
};

export default function Home() {
  const [resume, setResume] = useState("");
  const [job, setJob] = useState("");
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await fetch(baseUrl + "/api/v1/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_text: resume, job_description: job }),
      });
      if (!response.ok) throw new Error("Analysis request failed.");
      setResult(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <div className="container">
        <section className="hero">
          <h1>CareerFlow AI</h1>
          <p>Compare your resume with a job description, find skill gaps, and get practical suggestions before you apply.</p>
        </section>

        <form onSubmit={submit} className="grid">
          <section className="card">
            <h2>Your resume</h2>
            <textarea required minLength={20} value={resume}
              onChange={(e) => setResume(e.target.value)}
              placeholder="Paste your resume text here..." />
          </section>

          <section className="card">
            <h2>Job description</h2>
            <textarea required minLength={20} value={job}
              onChange={(e) => setJob(e.target.value)}
              placeholder="Paste the job description here..." />
          </section>

          <div>
            <button type="submit" disabled={loading}>
              {loading ? "Analyzing..." : "Analyze match"}
            </button>
          </div>
        </form>

        {error && <p role="alert">{error}</p>}

        {result && (
          <section className="card result">
            <h2>Analysis</h2>
            <p><strong>Match score:</strong> {result.match_score}%</p>
            <p><strong>Matched:</strong> {result.matched_skills.join(", ") || "None"}</p>
            <p><strong>Missing:</strong> {result.missing_skills.join(", ") || "None"}</p>
            <p><strong>ATS score:</strong> {result.ats_score}%</p>\n            <p><strong>Preferred matches:</strong> {result.preferred_matches.join(", ") || "None"}</p>\n            {result.ats_warnings.length > 0 && <><h3>ATS warnings</h3><ul>{result.ats_warnings.map((item) => <li key={item}>{item}</li>)}</ul></>}\n            <h3>Suggestions</h3>
            <ul>{result.suggestions.map((item) => <li key={item}>{item}</li>)}</ul>
          </section>
        )}
      </div>
    </main>
  );
}
