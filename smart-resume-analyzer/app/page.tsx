'use client';

import { ChangeEvent, FormEvent, useMemo, useState } from 'react';

type Result = { score:number; score_label:string; summary:string; green_flags:string[]; red_flags:string[]; recommendations:string[]; strengths:string[]; risks:string[]; matched_keywords:string[]; role_fit:string; sections:Record<string,boolean>; filename:string; target_role:string; job_description_provided:boolean; ai_enhanced:boolean; ai_notice?:string|null; word_count:number; };

const sampleResume = `HARSH VISHWAKARMA\nSoftware Developer | QA & Testing | Full-Stack Development\nMumbai, India | harshvish0987@gmail.com | github.com/harshvish0987-glitch\n\nPROFESSIONAL SUMMARY\nB.Sc. Information Technology graduate with hands-on project experience in Python, Flask, JavaScript, REST APIs and software testing.\n\nTECHNICAL SKILLS\nPython, JavaScript, SQL, HTML5, CSS3, Flask, React.js, Next.js, REST APIs, Gemini API, Firebase, Postman, Git/GitHub\n\nPROJECTS\nReal-Time Sign Language Translator\nBuilt a webcam-based gesture recognition application using MediaPipe and Flask. Tested varied lighting and hand positions and debugged frontend/backend integration.\n\nAI Chatbot Application\nDeveloped a conversational application integrating the Gemini API with a Flask backend. Tested malformed input and API failure scenarios.\n\nEDUCATION\nB.Sc. Information Technology — 2026`;

export default function Home(){
  const [file,setFile]=useState<File|null>(null); const [jd,setJd]=useState(''); const [role,setRole]=useState('Software Developer'); const [result,setResult]=useState<Result|null>(null); const [loading,setLoading]=useState(false); const [error,setError]=useState(''); const [sample,setSample]=useState('');
  const scoreClass = useMemo(()=> result ? result.score>=85?'excellent':result.score>=75?'strong':result.score>=60?'needs':'weak' : '',[result]);
  function onFile(e:ChangeEvent<HTMLInputElement>){ setFile(e.target.files?.[0]||null); setError(''); setResult(null); }
  async function analyze(e:FormEvent){e.preventDefault(); if(!file){setError('Choose a PDF, DOCX, or TXT resume first.');return;} setLoading(true);setError('');setResult(null); try{const fd=new FormData();fd.append('resume',file);fd.append('job_description',jd);fd.append('target_role',role);const r=await fetch('/api/analyze',{method:'POST',body:fd});const data=await r.json();if(!r.ok)throw new Error(data.error||'Analysis failed');setResult(data);}catch(err:any){setError(err.message||'Something went wrong.');}finally{setLoading(false);}}
  function loadSample(){const blob=new Blob([sampleResume],{type:'text/plain'});setFile(new File([blob],'sample-resume.txt',{type:'text/plain'}));setSample('Sample resume loaded. Add a job description and analyze it.');setError('');setResult(null);}
  function reset(){setFile(null);setJd('');setResult(null);setError('');setSample('');}
  function downloadReport(){if(!result)return;const html=`<html><head><title>Resume Analysis</title><style>body{font-family:Arial;padding:40px;color:#172033}h1{font-size:28px}.score{font-size:48px;font-weight:700}.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}li{margin:8px 0}</style></head><body><h1>Smart Resume Analyzer Report</h1><p>${result.filename}</p><div class="score">${result.score}/100</div><p>${result.summary}</p><div class="grid"><section><h2>Green Flags</h2><ul>${result.green_flags.map(x=>`<li>${x}</li>`).join('')}</ul></section><section><h2>Red Flags</h2><ul>${result.red_flags.map(x=>`<li>${x}</li>`).join('')}</ul></section></div><h2>Recommendations</h2><ul>${result.recommendations.map(x=>`<li>${x}</li>`).join('')}</ul><h2>Matched Keywords</h2><p>${result.matched_keywords.join(', ')}</p></body></html>`;const w=window.open('','_blank');if(w){w.document.write(html);w.document.close();w.focus();w.print();}}
  return <main>
    <nav className="nav"><div className="brand">SMART<span>RESUME</span></div><div className="nav-note">AI-assisted ATS analysis</div></nav>
    <section className="hero"><div className="eyebrow">RESUME INTELLIGENCE</div><h1>Know exactly what a recruiter will notice.</h1><p>Upload your resume, optionally add a target job description, and get an explainable score, ATS keyword alignment, green flags, red flags, and specific improvements.</p><div className="hero-actions"><button className="ghost" onClick={loadSample}>Load sample resume</button><span>PDF, DOCX and TXT supported</span></div></section>
    <section className="workspace">
      <form className="panel form-panel" onSubmit={analyze}>
        <div className="panel-head"><div><div className="kicker">01</div><h2>Resume input</h2></div><button type="button" className="text-btn" onClick={reset}>Reset</button></div>
        <label className="dropzone"><input type="file" accept=".pdf,.docx,.txt" onChange={onFile}/><strong>{file?file.name:'Drop your resume here'}</strong><span>{file?'Ready for analysis':'or click to choose a file'}</span></label>
        <label>Target role<select value={role} onChange={e=>setRole(e.target.value)}><option>Software Developer</option><option>QA / Software Tester</option><option>Full-Stack Developer</option><option>Python Developer</option><option>General IT</option></select></label>
        <label>Job description <span className="optional">optional</span><textarea value={jd} onChange={e=>setJd(e.target.value)} placeholder="Paste the job description here for role-specific ATS matching..." rows={9}/></label>
        {error&&<div className="error">{error}</div>}{sample&&<div className="notice">{sample}</div>}
        <button className="primary" disabled={loading}>{loading?'Analyzing resume...':'Analyze resume'}</button>
        <p className="fine">Your Gemini API key stays server-side. The analyzer uses deterministic checks first and AI enhancement when the API is configured.</p>
      </form>
      <section className="panel result-panel">
        {!result ? <div className="empty"><div className="empty-mark">SR</div><h2>Your analysis will appear here</h2><p>Upload a resume to calculate a baseline score and generate recruiter-focused findings.</p><div className="checks"><span>Explainable score</span><span>Green flags</span><span>Red flags</span><span>ATS alignment</span><span>Actionable fixes</span></div></div> : <>
          <div className="result-top"><div><div className="kicker">ANALYSIS COMPLETE</div><h2>{result.filename}</h2><p>{result.word_count} extracted words · {result.ai_enhanced?'Gemini enhanced':'Deterministic baseline'}</p></div><button className="ghost" onClick={downloadReport}>Print / PDF report</button></div>
          {result.ai_notice&&<div className="notice">{result.ai_notice}</div>}
          <div className="score-card"><div className={`score-ring ${scoreClass}`}><strong>{result.score}</strong><span>/100</span></div><div><div className="score-label">{result.score_label}</div><p>{result.summary}</p></div></div>
          <div className="metrics"><div><span>Role fit</span><strong>{result.target_role}</strong></div><div><span>Job description</span><strong>{result.job_description_provided?'Matched':'Not provided'}</strong></div><div><span>Keywords</span><strong>{result.matched_keywords.length}</strong></div></div>
          <div className="two-col"><Flag title="Green flags" items={result.green_flags} good/><Flag title="Red flags" items={result.red_flags}/></div>
          <div className="section"><div className="section-title"><span>Recommended next moves</span></div><ul className="recommendations">{result.recommendations.map((x,i)=><li key={i}>{x}</li>)}</ul></div>
          <div className="section"><div className="section-title"><span>Matched ATS terms</span></div><div className="chips">{result.matched_keywords.length?result.matched_keywords.map(k=><span key={k}>{k}</span>):<em>Add a job description to see job-specific keyword alignment.</em>}</div></div>
        </>}
      </section>
    </section>
    <footer>Smart Resume Analyzer & ATS Checker · Built with Next.js, React, Flask, Python, Gemini API, Firebase and SQL.</footer>
  </main>
}
function Flag({title,items,good=false}:{title:string;items:string[];good?:boolean}){return <div className={`flag-box ${good?'good':''}`}><div className="section-title"><span>{title}</span><b>{items.length}</b></div><ul>{items.length?items.map((x,i)=><li key={i}>{x}</li>):<li>No major issues detected in this category.</li>}</ul></div>}
