/**
 * CV Auto-Builder — Layout B, 2-page max
 * Ajao Abiola Olanrewaju — Research / Data / Analytics roles
 *
 * Usage: node cv_builder.js '<JSON_STRING>' '<OUTPUT_DIR>'
 * JSON shape: { title, company, salary, location, source, apply_link }
 *
 * RULES — DO NOT CHANGE:
 * - UoM/Manitoba project: NO hyperlink ever (NDA). Plain text only.
 * - Telecom client: "a leading Nigerian telecommunications brand" — NEVER name MTN
 * - Binatone and Mable = direct full-time employment (NOT consulting)
 * - LinkedIn / GitHub always hyperlinked in contact and portfolio
 * - Never invent experience, tools, metrics or certifications not in this file
 */

const {
  Document, Packer, Paragraph, TextRun, AlignmentType, BorderStyle,
  TabStopType, ExternalHyperlink, UnderlineType
} = require('docx');
const fs = require('fs');

// ── COLOURS & SIZES ──────────────────────────────────────────────────────────
const NAVY   = '1F4E79';
const MID    = '2E74B5';
const DARK   = '1A1A1A';
const GREY   = '595959';
const FONT   = 'Calibri';

const pt = n => n * 2;  // docx half-points

// ── HELPERS ──────────────────────────────────────────────────────────────────
const bold   = (t, sz, col=DARK) => new TextRun({ text:t, bold:true,    size:sz, color:col, font:FONT });
const normal = (t, sz, col=DARK) => new TextRun({ text:t,               size:sz, color:col, font:FONT });
const italic = (t, sz, col=GREY) => new TextRun({ text:t, italics:true, size:sz, color:col, font:FONT });

const link = (text, url, sz) => new ExternalHyperlink({
  link: url,
  children: [new TextRun({ text, size:sz, color:MID, font:FONT, underline:{ type:UnderlineType.SINGLE } })],
});

const sectionHead = (title) => new Paragraph({
  children: [bold(title.toUpperCase(), pt(10.5), NAVY)],
  spacing: { before:200, after:60 },
  border: { bottom: { color:NAVY, space:1, style:BorderStyle.SINGLE, size:8 } },
});

const bullet = (leadLabel, rest, extraRuns=[]) => new Paragraph({
  children: leadLabel
    ? [bold('▸ ', pt(9.5), MID), bold(leadLabel+': ', pt(9.5)), normal(rest, pt(9.5)), ...extraRuns]
    : [bold('▸ ', pt(9.5), MID), normal(rest, pt(9.5)), ...extraRuns],
  spacing: { before:36, after:36 },
  indent: { left:360 },
});

const jobTitle = (title, dates) => new Paragraph({
  children: [
    bold(title, pt(10), NAVY),
    italic('\t'+dates, pt(9.5)),
  ],
  tabStops: [{ type:TabStopType.RIGHT, position:9360 }],
  spacing: { before:140, after:20 },
});

const jobOrg = (org) => new Paragraph({
  children: [italic(org, pt(9.5))],
  spacing: { before:0, after:50 },
});

const skillRow = (label, value) => new Paragraph({
  children: [bold(label+':  ', pt(9.5), NAVY), normal(value, pt(9.5))],
  spacing: { before:36, after:36 },
});

// ── TITLE ADAPTATION ─────────────────────────────────────────────────────────
function adaptTitle(jobTitle) {
  return jobTitle.replace(/[^a-zA-Z0-9\s\-&\/(),.]/g, '').trim();
}

// ── SKILL ROWS — only confirmed tools ────────────────────────────────────────
function adaptSkills(jobTitle) {
  const t = jobTitle.toLowerCase();

  const BASE = [
    ['Data Analysis & Reporting',
     'Python (Pandas, NumPy, NLP), R, SPSS, SQL, Advanced Excel (Power Query, XLOOKUP), statistical and thematic analysis'],
    ['Dashboard & Visual Analytics',
     'Power BI (DAX, calculated columns, real-time KPIs), Tableau, Looker Studio, Excel Power Query'],
    ['AI & Automation Tools',
     'Advanced prompt engineering (ChatGPT, Claude, Gemini, Perplexity), n8n workflow automation, NLP-driven qualitative coding, automated QA pipelines, Gemini API (client-side tooling)'],
    ['Research & M&E',
     'Quantitative & qualitative study design, survey scripting (KoboToolbox, SurveyCTO, ODK), CATI/CAPI, mixed-methods, donor-facing M&E reporting (BMGF-funded projects)'],
    ['Performance & Operational Analytics',
     'KPI framework design, workforce performance reporting, project tracking, real-time operational dashboards, timesheet and contract data management'],
    ['Communication & Capacity Building',
     'Executive reports, policy briefs, training materials, stakeholder presentations, cross-functional team support'],
  ];

  if (t.includes('data') || t.includes('bi') || t.includes('analytics')) {
    return [BASE[0], BASE[2], BASE[1], BASE[3], BASE[4], BASE[5]];
  } else if (t.includes('market') || t.includes('competitive') || t.includes('intelligence')) {
    return [BASE[3], BASE[0], BASE[1], BASE[2], BASE[5], BASE[4]];
  } else if (t.includes('performance') || t.includes('kpi') || t.includes('operational')) {
    return [BASE[4], BASE[1], BASE[0], BASE[2], BASE[3], BASE[5]];
  } else if (t.includes('scientist') || t.includes('ml') || t.includes('ai')) {
    return [BASE[2], BASE[0], BASE[3], BASE[1], BASE[5], BASE[4]];
  }
  return BASE;
}

// ── SUMMARY ADAPTATION ───────────────────────────────────────────────────────
function adaptSummary(jobTitle) {
  const t = jobTitle.toLowerCase();
  let focus = 'quantitative and qualitative research, market intelligence, and data-driven insight delivery across health, governance, energy, and digital sectors in Nigeria';

  if (t.includes('performance') || t.includes('operational') || t.includes('kpi')) {
    focus = 'performance analytics, KPI reporting, and operational intelligence across research, health systems, and commercial environments in Nigeria';
  } else if (t.includes('data') && !t.includes('market')) {
    focus = 'data analysis, business intelligence, and automated reporting across health, governance, energy access, and digital sectors in Nigeria';
  } else if (t.includes('market') || t.includes('marketing') || t.includes('competitive')) {
    focus = 'market research, consumer intelligence, and competitive analysis across FMCG, telecommunications, and digital sectors in Nigeria';
  } else if (t.includes('scientist') || t.includes('ai') || t.includes('ml')) {
    focus = 'applied data science, NLP, and AI-assisted analytics across consumer research, public health, and organisational intelligence in Nigeria';
  }

  return `Data and research analytics professional with 7+ years of experience in ${focus}. `
    + `Holds a B.Tech in Physics Electronics (FUTA, Second Class Upper) and a Master's in Collective Intelligence (UM6P, Morocco, 75% Mention Bien). `
    + `Builds production-grade AI tools and dashboards — including a Bayesian CATI contact-scoring system (31,946 records), `
    + `a Gemini-powered survey data preparation SaaS (SPSS + XLSForm generation in under 2 minutes), and real-time Power BI reporting deployed at NOI Polls. `
    + `Proficient in Python, R, SPSS, SQL, Power BI, KoboToolbox, SurveyCTO, and advanced prompt engineering, with a track record of delivering rigorous, decision-ready analysis independently and at pace.`;
}

// ── BUILD CV ─────────────────────────────────────────────────────────────────
function buildCV(job) {
  const cvTitle = adaptTitle(job.title);
  const skills  = adaptSkills(job.title);
  const summary = adaptSummary(job.title);

  const doc = new Document({
    styles: {
      default: {
        document: { run: { font:FONT, size:pt(9.5), color:DARK } },
      },
    },
    sections: [{
      properties: {
        page: {
          margin: { top:1008, bottom:1008, left:1134, right:1134 },  // ~1.8cm sides
          size: { width:12240, height:15840 },
        },
      },
      children: [

        // ── NAME ──
        new Paragraph({
          children: [bold('AJAO ABIOLA OLANREWAJU', pt(18), NAVY)],
          alignment: AlignmentType.CENTER,
          spacing: { before:0, after:40 },
        }),

        // ── TITLE LINE ──
        new Paragraph({
          children: [bold(cvTitle, pt(11.5), MID)],
          alignment: AlignmentType.CENTER,
          spacing: { before:0, after:60 },
        }),

        // ── CONTACT ──
        new Paragraph({
          children: [
            normal('ajaoabiola0812@gmail.com  |  +234 808 8414 644  |  ', pt(9), GREY),
            link('linkedin.com/in/abiola-ajao', 'https://www.linkedin.com/in/abiola-ajao', pt(9)),
            normal('  |  ', pt(9), GREY),
            link('github.com/Abiola97/All-Projects', 'https://github.com/Abiola97/All-Projects', pt(9)),
            normal('  |  Nigeria (Open to Remote)', pt(9), GREY),
          ],
          alignment: AlignmentType.CENTER,
          spacing: { before:0, after:100 },
        }),

        // ── PROFESSIONAL SUMMARY ──
        sectionHead('Professional Summary'),
        new Paragraph({
          children: [normal(summary, pt(9.5))],
          spacing: { before:60, after:40 },
        }),

        // ── CORE SKILLS ──
        sectionHead('Core Skills'),
        ...skills.map(([label, value]) => skillRow(label, value)),

        // ── WORK EXPERIENCE ──
        sectionHead('Work Experience'),

        // NOI Polls — Senior Research & Data Analyst
        jobTitle('Senior Research & Data Analyst', 'Mar 2026 – Present'),
        jobOrg('NOI Polls, Abuja, Nigeria · Full-time'),
        bullet('Performance Dashboards',
          'Built real-time Power BI dashboards tracking field operations KPIs — data validity rates, enumerator productivity, and submission timelines — across 10+ concurrent CATI/CAPI studies nationwide.'),
        bullet('AI-Assisted Reporting',
          'Applied advanced prompt engineering (ChatGPT, Claude) to automate report drafting, meeting minutes, and terms of reference — reducing document turnaround time by 30% while maintaining client-ready quality.'),
        bullet('Data Quality & Validation',
          'Engineered Python (Pandas) QA pipelines achieving 99% data validity on 3,000+ records from a BMGF-funded health facility assessment across seven Nigerian states.'),
        bullet('Capacity Building',
          'Developed training materials and facilitated knowledge-transfer sessions for 15+ field staff on digital data collection tools and QA protocols; coordinated logistics for multi-state training rollouts.'),

        // Vala Bleu
        jobTitle('Research Analyst — Digital Performance & Competitive Intelligence', 'May 2025 – Feb 2026'),
        jobOrg('Vala Bleu, Morocco · Hybrid'),
        bullet('Visual Analytics',
          'Consolidated data from 300+ indexed sources into Power BI dashboards surfacing conversion bottlenecks that drove a 20% increase in customer conversion within three months.'),
        bullet('Automated Reporting',
          'Built automated pipelines tracking impressions, CTR, and engagement metrics, reducing stakeholder reporting lag and improving brand visibility by 15%.'),
        bullet('AI Content Production',
          'Used generative AI tools to produce high-quality reports, correspondence, and performance briefs aligned to organisational standards — reducing content production time by 40%.'),

        // Binatone
        jobTitle('Research Analyst — Market Intelligence & Consumer Insights', 'Feb 2024 – Nov 2024'),
        jobOrg('Binatone Nigeria, Lagos · Full-time (Direct Employment)'),
        bullet('Operational KPI Dashboards',
          'Built Power BI dashboards tracking product availability and display compliance across 200 retail outlets — improving restocking compliance to 82% and display compliance to 91%.'),
        bullet('Workforce Analytics',
          'Designed performance-tracking frameworks for field agents; presented monthly performance summaries to senior management.'),
        bullet('Evidence-Based Reporting',
          'Delivered competitive intelligence and consumer insight reports that drove 84% of annual sales target within six months.'),

        // AASIT
        jobTitle('Research Analyst — Field Research & Operational Intelligence', 'Oct 2022 – Dec 2023'),
        jobOrg('AASIT Consulting, Lagos · Full-time'),
        bullet('Large-Scale Field Coordination',
          'Coordinated multi-state field operations across 5 Nigerian states, managing 50+ field agents and ensuring data quality and submission timelines for high-value client projects.'),
        bullet('Digital Tools Adoption',
          'Championed adoption of KoboToolbox and SurveyCTO, designing scripted questionnaires and QA protocols that reduced data error rates by 35%.'),

        // Mable
        jobTitle('Data Analyst & Research Associate', 'Jan 2019 – May 2021'),
        jobOrg('Mable, Lagos · Full-time (Direct Employment)'),
        bullet('Performance Analytics',
          'Designed and maintained Excel-based operational trackers and analytical models supporting business decision-making across HR and commercial functions.'),
        bullet('Research & Reporting',
          'Conducted primary and secondary research, producing structured reports and presentations for internal and external stakeholders.'),

        // ── RECENT PROJECTS ──
        sectionHead('Recent Projects'),

        // UoM/Manitoba — NO hyperlink (NDA)
        bullet('',
          'University of Manitoba — MNCH Health Facility Assessment (NOI Polls, 2026): End-to-end data management for a maternal and child health needs assessment across 7 Nigerian states, achieving 99% data validity on 3,000+ field records across primary, secondary, and tertiary facility levels.'),

        // BMGF / MAMII Skills Retention Assessment
        bullet('',
          'BMGF Skills Retention Assessment (NOI Polls, 2025–2026): Quantitative analysis of training retention and skill-mix data for a BMGF-funded maternal health programme; produced donor-facing dashboards and evidence briefs informing national capacity-building strategy.'),

        // CATI Contact Intelligence System
        new Paragraph({
          children: [
            bold('▸ ', pt(9.5), MID),
            normal('CATI Contact Intelligence System (NOI Polls, 2026): Bayesian propensity-scoring SPA built in vanilla JS + Google Sheets API, scoring 31,946 respondent records into priority tiers (SHA-256 anonymised, NDPA 2023 compliant). ', pt(9.5)),
            link('[Live Tool]', 'https://response-rate-for-cati-survey.abiolaolanrewaju1.workers.dev/', pt(9.5)),
          ],
          spacing: { before:36, after:36 },
          indent: { left:360 },
        }),

        // DataPrep
        new Paragraph({
          children: [
            bold('▸ ', pt(9.5), MID),
            normal('DataPrep — Survey Data Prep SaaS (NOI Polls, 2026): Gemini-powered browser tool generating SPSS syntax, XLSForm scripts, and thematic clusters from uploaded questionnaires in under 2 minutes; validated on a 335-row XLSForm with full skip logic. ', pt(9.5)),
            link('[Live Tool]', 'https://dataprep-spss-and-xls-formdesign.abiolaolanrewaju1.workers.dev/', pt(9.5)),
          ],
          spacing: { before:36, after:36 },
          indent: { left:360 },
        }),

        // BizIntel Enterprise
        new Paragraph({
          children: [
            bold('▸ ', pt(9.5), MID),
            normal('BizIntel Enterprise — Organisational Feedback Analytics Platform (2026): Collective-intelligence-driven SaaS collecting and clustering employee/stakeholder feedback into sentiment dashboards and executive PowerPoint exports. ', pt(9.5)),
            link('[Live Platform]', 'https://bizintel-enterprise.vercel.app/', pt(9.5)),
          ],
          spacing: { before:36, after:36 },
          indent: { left:360 },
        }),

        // ── EDUCATION ──
        sectionHead('Education'),

        new Paragraph({
          children: [
            bold("MSc Collective Intelligence", pt(9.5), NAVY),
            italic('\tMohammed VI Polytechnic University (UM6P), Morocco · 2024–2026', pt(9.5)),
          ],
          tabStops: [{ type:TabStopType.RIGHT, position:9360 }],
          spacing: { before:60, after:20 },
        }),
        new Paragraph({
          children: [italic('Grade: 75% — Mention Bien  |  Focus: data systems, collective decision-making, AI applications, MEL, Behavioural Science', pt(9.5))],
          spacing: { before:0, after:50 },
          indent: { left:360 },
        }),

        new Paragraph({
          children: [
            bold('B.Tech Physics Electronics (Second Class Upper)', pt(9.5), NAVY),
            italic('\tFederal University of Technology Akure (FUTA) · 2013–2018', pt(9.5)),
          ],
          tabStops: [{ type:TabStopType.RIGHT, position:9360 }],
          spacing: { before:40, after:50 },
        }),

        // ── PORTFOLIO ──
        sectionHead('Portfolio & Profiles'),
        new Paragraph({
          children: [
            bold('GitHub: ', pt(9.5), NAVY),
            link('github.com/Abiola97/All-Projects', 'https://github.com/Abiola97/All-Projects', pt(9.5)),
            normal('   |   ', pt(9.5), GREY),
            bold('LinkedIn: ', pt(9.5), NAVY),
            link('linkedin.com/in/abiola-ajao', 'https://www.linkedin.com/in/abiola-ajao', pt(9.5)),
            normal('   |   ', pt(9.5), GREY),
            bold('Tableau: ', pt(9.5), NAVY),
            link('public.tableau.com/app/profile/abiola.ajao', 'https://public.tableau.com/app/profile/abiola.ajao', pt(9.5)),
          ],
          spacing: { before:60, after:60 },
        }),

      ],
    }],
  });

  return doc;
}

// ── MAIN ─────────────────────────────────────────────────────────────────────
async function main() {
  let job = {};
  try {
    job = JSON.parse(process.argv[2] || '{}');
  } catch(e) {
    job = { title: 'Research Analyst', company: 'Unknown', location: 'Nigeria' };
  }

  const outDir = process.argv[3] || __dirname;
  const safeTitle   = (job.title   || 'Analyst').replace(/[^a-zA-Z0-9]/g, '_').substring(0, 30);
  const safeCompany = (job.company || 'Company').replace(/[^a-zA-Z0-9]/g, '_').substring(0, 20);
  const filename = `Ajao_Abiola_${safeTitle}_${safeCompany}_CV.docx`;
  const outPath  = `${outDir}/${filename}`;

  const doc = buildCV(job);
  const buf = await Packer.toBuffer(doc);
  fs.writeFileSync(outPath, buf);
  console.log(outPath);
}

main().catch(e => { console.error(e); process.exit(1); });
