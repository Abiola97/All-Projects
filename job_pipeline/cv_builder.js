/**
 * CV Auto-Builder — Layout B with hyperlinks
 * Ajao Abiola Olanrewaju — Research / Data / Analytics roles
 *
 * Usage: node cv_builder.js '<JSON_STRING>'
 * JSON shape: { title, company, salary, location, source, apply_link }
 *
 * Rules:
 * - UoM/Manitoba project: NO hyperlink ever (NDA). Plain text only.
 * - Telecom client: "a leading Nigerian telecommunications brand" — NOT MTN
 * - Binatone and Mable = direct full-time employment
 * - LinkedIn / GitHub / Tableau / cert hyperlinks embedded
 */

const {
  Document, Packer, Paragraph, TextRun, AlignmentType, BorderStyle,
  TabStopType, ExternalHyperlink, HeadingLevel
} = require('docx');
const fs = require('fs');

// ── COLOURS & SIZES ──────────────────────────────────────────────────────────
const DARK_BLUE = '1F4E79';
const MID_BLUE  = '2E74B5';
const BLACK     = '000000';
const GREY      = '595959';
const BODY = 18;   // 9pt
const SMALL = 16;  // 8pt
const HEAD  = 28;  // 14pt
const SUB   = 20;  // 10pt

// ── HELPERS ──────────────────────────────────────────────────────────────────
const bold   = (t, sz=BODY, col=BLACK) => new TextRun({ text:t, bold:true,   size:sz, color:col, font:'Calibri' });
const normal = (t, sz=BODY, col=BLACK) => new TextRun({ text:t,              size:sz, color:col, font:'Calibri' });
const italic = (t, sz=BODY, col=BLACK) => new TextRun({ text:t, italics:true,size:sz, color:col, font:'Calibri' });

const link = (text, url, sz=SMALL, col=MID_BLUE) => new ExternalHyperlink({
  link: url,
  children: [new TextRun({ text, size:sz, color:col, font:'Calibri', underline:{} })],
});

const sectionHeader = (title) => new Paragraph({
  children: [new TextRun({ text:title.toUpperCase(), bold:true, size:SUB, color:DARK_BLUE, font:'Calibri' })],
  spacing: { before:160, after:50 },
  border: { bottom: { color:DARK_BLUE, space:1, style:BorderStyle.SINGLE, size:6 } },
});

const bullet = (boldPart, rest, extraRuns=[]) => new Paragraph({
  children: boldPart
    ? [bold('▸ ', BODY, DARK_BLUE), bold(boldPart+': ', BODY, BLACK), normal(rest, BODY, BLACK), ...extraRuns]
    : [bold('▸ ', BODY, DARK_BLUE), normal(rest, BODY, BLACK), ...extraRuns],
  spacing: { before:30, after:30 },
  indent: { left:160 },
});

const roleHeader = (title, dates) => new Paragraph({
  children: [
    new TextRun({ text:title, bold:true, size:SUB, color:DARK_BLUE, font:'Calibri' }),
    new TextRun({ text:'\t'+dates, size:BODY, color:GREY, font:'Calibri' }),
  ],
  tabStops: [{ type:TabStopType.RIGHT, position:9360 }],
  spacing: { before:100, after:0 },
});

const companyLine = (company, location) => new Paragraph({
  children: [italic(company+', ', BODY, MID_BLUE), italic(location, BODY, GREY)],
  spacing: { before:0, after:40 },
});

const skillRow = (label, value) => new Paragraph({
  children: [bold(label+': ', BODY), normal(value, BODY)],
  spacing: { before:20, after:20 },
});

// ── TITLE ADAPTATION ─────────────────────────────────────────────────────────
function adaptTitle(jobTitle) {
  // Clean and use exact JD title
  return jobTitle.replace(/[^a-zA-Z0-9\s\-&\/(),.]/g, '').trim();
}

// ── SKILL ROW ADAPTATION ─────────────────────────────────────────────────────
function adaptSkills(jobTitle) {
  const t = jobTitle.toLowerCase();
  let skills = [
    ['Research Design & Execution', 'Quantitative & qualitative study design, survey scripting (KoboToolbox, SurveyCTO, ODK), CATI/CAPI operations, sampling plans, mixed-methods research'],
    ['Data Analysis & Reporting', 'SPSS, R, Python (Pandas, NLP), SQL, Advanced Excel (Power Query, XLOOKUP), Power BI (DAX), Tableau, Looker Studio, statistical and thematic analysis'],
    ['Market & Competitive Intelligence', 'Primary and secondary market research, sector trend analysis, competitive landscape mapping, consumer profiling, energy access and emerging technology research'],
    ['AI & Automation Tools', 'ChatGPT, Claude, Perplexity, n8n workflow automation, NLP-driven qualitative coding, automated QA pipelines, Generative AI prompt engineering'],
    ['Insight Communication', 'Executive research reports, policy briefs, stakeholder presentations, donor-facing M&E reporting, data storytelling for non-technical audiences'],
    ['Field & Project Management', 'Field team coordination (50+ agents), data quality assurance, multi-project management, cross-functional collaboration, budget tracking'],
  ];

  // Re-order based on role focus
  if (t.includes('data') || t.includes('bi') || t.includes('analytics')) {
    skills = [
      skills[1],  // Data Analysis first
      skills[3],  // AI & Automation
      skills[2],  // Market Intelligence
      skills[0],  // Research Design
      skills[4],  // Insight Communication
      skills[5],  // Field & Project Mgmt
    ];
  } else if (t.includes('market') || t.includes('competitive') || t.includes('intelligence')) {
    skills = [
      skills[2],  // Market Intelligence first
      skills[0],  // Research Design
      skills[1],  // Data Analysis
      skills[3],  // AI
      skills[4],  // Communication
      skills[5],  // Field & PM
    ];
  } else if (t.includes('scientist') || t.includes('ml') || t.includes('ai')) {
    skills = [
      skills[3],  // AI first
      skills[1],  // Data Analysis
      skills[0],  // Research Design
      skills[2],  // Market Intel
      skills[4],  // Communication
      skills[5],  // PM
    ];
  }
  return skills;
}

// ── SUMMARY ADAPTATION ───────────────────────────────────────────────────────
function adaptSummary(jobTitle) {
  const t = jobTitle.toLowerCase();
  let focus = 'quantitative and qualitative research, competitive intelligence, and market analysis across energy access, financial inclusion, health systems, and digital sectors in Nigeria and West Africa';
  if (t.includes('data') && !t.includes('market')) {
    focus = 'data analysis, business intelligence, and data-driven decision support across energy access, financial inclusion, health systems, and digital sectors in Nigeria and West Africa';
  } else if (t.includes('market') || t.includes('marketing')) {
    focus = 'market research, consumer intelligence, and competitive analysis across energy access, FMCG, telecommunications, and digital sectors in Nigeria and West Africa';
  } else if (t.includes('scientist') || t.includes('ai') || t.includes('ml')) {
    focus = 'applied data science, machine learning, NLP, and AI-assisted analytics across consumer research, financial inclusion, and public sector intelligence in Nigeria and West Africa';
  }

  return `Research and Data professional with 4+ years of experience executing ${focus}. `
    + `Grounded in a B.Tech. Physics Electronics degree (FUTA) and a Master's in Collective Intelligence (UM6P, Morocco, 75% Mention Bien). `
    + `Experienced managing multi-source data pipelines, field operations, and structured insight delivery for government, donor, and private sector clients. `
    + `Proficient in SPSS, R, Python, Power BI, KoboToolbox, SurveyCTO, and AI-assisted research tools, with a track record of delivering rigorous, decision-ready findings independently and at pace.`;
}

// ── BUILD CV ─────────────────────────────────────────────────────────────────
function buildCV(job) {
  const cvTitle  = adaptTitle(job.title);
  const skills   = adaptSkills(job.title);
  const summary  = adaptSummary(job.title);

  const doc = new Document({
    sections: [{
      properties: {
        page: {
          margin: { top:720, bottom:720, left:900, right:900 },
          size: { width:12240, height:15840 },
        },
      },
      children: [

        // ── NAME ──
        new Paragraph({
          children: [new TextRun({ text:'AJAO ABIOLA OLANREWAJU', bold:true, size:HEAD, color:DARK_BLUE, font:'Calibri' })],
          alignment: AlignmentType.CENTER,
          spacing: { before:0, after:40 },
        }),

        // ── TITLE LINE ──
        new Paragraph({
          children: [new TextRun({ text: cvTitle + ' | Energy, Climate & Market Intelligence', bold:true, size:SUB, color:MID_BLUE, font:'Calibri' })],
          alignment: AlignmentType.CENTER,
          spacing: { before:0, after:60 },
        }),

        // ── CONTACT with hyperlinks ──
        new Paragraph({
          children: [
            normal('ajaoabiola0812@gmail.com', SMALL, GREY),
            normal('  |  +234 808 8414 644  |  ', SMALL, GREY),
            link('linkedin.com/in/abiola-ajao', 'https://www.linkedin.com/in/abiola-ajao', SMALL),
            normal('  |  ', SMALL, GREY),
            link('github.com/Abiola97/All-Projects', 'https://github.com/Abiola97/All-Projects', SMALL),
            normal('  |  Nigeria (Open to Remote)', SMALL, GREY),
          ],
          alignment: AlignmentType.CENTER,
          spacing: { before:0, after:80 },
        }),

        // ── PROFESSIONAL SUMMARY ──
        sectionHeader('Professional Summary'),
        new Paragraph({
          children: [normal(summary, BODY)],
          spacing: { before:60, after:40 },
        }),

        // ── CORE SKILLS ──
        sectionHeader('Core Skills'),
        ...skills.map(([label, value]) => skillRow(label, value)),

        // ── WORK EXPERIENCE ──
        sectionHeader('Work Experience'),

        // NOI Polls
        roleHeader('Research Analyst (Survey & Market Intelligence)', 'Mar 2026 – Present'),
        companyLine('NOI Polls', 'Abuja, Nigeria · Full-time'),
        bullet('Research Design & Execution', 'Independently lead medium-to-large CATI/CAPI research projects across health, governance, energy access, and social sectors — designing questionnaires, sampling plans, and discussion guides for 10+ concurrent studies across Nigeria.'),
        bullet('Data Quality & Validation', 'Applied automated Python (Pandas) QA scripts to achieve 99% data validity on 3,000+ records from a health facility assessment across seven Nigerian states.'),
        bullet('AI-Assisted Intelligence', 'Deployed AI tools (ChatGPT, Claude, Perplexity) to automate data summarisation, thematic coding, and insight generation — cutting report turnaround time by 30% without sacrificing analytical depth.'),
        bullet('Stakeholder Reporting', 'Produced structured intelligence reports and client presentations for government and private sector decision-makers, including monthly governance, power supply, and personal wellbeing index analytics.'),

        // Vala Bleu
        roleHeader('Research Analyst (Digital Performance & Competitive Intelligence)', 'May 2025 – Feb 2026'),
        companyLine('Vala Bleu', 'Morocco · Hybrid'),
        bullet('Competitive Intelligence', 'Designed and executed quantitative and qualitative digital research consolidating data from 300+ indexed pages into Power BI dashboards — surfacing conversion bottlenecks that drove a 20% increase in customer conversion within three months.'),
        bullet('Insight Reporting', 'Automated reporting pipelines tracking impressions, CTR, and audience engagement metrics, improving brand visibility by 15% and reducing stakeholder reporting lag.'),
        bullet('Research Documentation', 'Developed reusable research templates and data definitions, improving consistency and reproducibility across all reporting cycles.'),

        // Binatone
        roleHeader('Research Analyst (Market Intelligence & Consumer Insights)', 'Feb 2024 – Nov 2024'),
        companyLine('Binatone Nigeria', 'Lagos, Nigeria · Full-time'),
        bullet('Market Research', 'Designed and executed quantitative consumer surveys across 200 retail outlets, identifying high-utility product segments and behavioural patterns that drove 84% of the annual sales target within six months.'),
        bullet('Competitive Analysis', 'Monitored retail market trends and consumer data, delivering competitive intelligence to C-suite executives that increased repeat purchases by 20% and informed product positioning strategy.'),
        bullet('Intelligence Dashboards', 'Built automated Power BI dashboards tracking product availability and display compliance in real time, improving restocking compliance to 82% and display compliance to 91%.'),

        // AASIT
        roleHeader('Research Analyst (Field Research & Sectoral Intelligence)', 'Oct 2022 – Dec 2023'),
        companyLine('AASIT Consulting', 'Lagos, Nigeria · Full-time'),
        bullet('Large-Scale Research Management', 'Designed and coordinated multi-state field research operations, collecting and validating datasets from 20,000+ respondents to inform fintech product expansion and financial inclusion strategy.'),
        bullet('Behavioural & Gap Analysis', 'Applied exploratory research and NLP-driven qualitative analysis to quantify financial inclusion gaps, producing evidence-backed recommendations that contributed to a 20% increase in community-level financial engagement.'),
        bullet('Field Operations', 'Coordinated 50+ field agents across multiple geographies using KoboToolbox and ODK, maintaining quality standards and translating raw field data into structured, client-ready findings.'),

        // D-Aggregate
        roleHeader('Research & Data Analyst (Retail Market Intelligence)', 'Sept 2021 – Sept 2022'),
        companyLine('D-Aggregate Nigeria', 'Lagos, Nigeria · Hybrid'),
        bullet('Market Research & Analytics', 'Coordinated fieldwork across 1,000 retail outlets and conducted quantitative analysis to measure product shelf visibility — achieving 78% visibility across five business regions via retail audit BI tools.'),
        bullet('Competitive Intelligence', 'Produced market intelligence on Share of Shelf and Most Stock List metrics, informing the operations strategy of 194 merchandisers and 19 area supervisors across Nigeria.'),
        bullet('SME Research & Donor Reporting', 'Managed a research database covering 6,000+ youth-led SMEs, producing trend analyses and structured reports that directly informed Lagos State Employment Trust Fund strategy.'),

        // ── KEY RESEARCH PROJECTS ──
        sectionHeader('Key Research Projects'),
        // UoM project: NO hyperlink — plain text only (NDA)
        bullet('', 'University of Manitoba — MNCH Health Facility Assessment (NOI Polls, 2026): End-to-end data management for a MNCH needs assessment across 7 Nigerian states, achieving 99% data validity on 3,000+ field records across primary, secondary, and tertiary health facility levels.'),
        bullet('', 'Energy & Telecom Consumer Segmentation Study (NOI Polls, 2026): Mixed-methods segmentation study for a leading Nigerian telecommunications brand across 5 states — combining 2,000+ survey responses with NLP-driven qualitative analysis to surface strategic repositioning recommendations for the energy access and connectivity market.'),
        new Paragraph({
          children: [
            bold('▸ ', BODY, DARK_BLUE),
            normal('BizIntel Enterprise — AI-Powered Consumer Research Platform (UM6P Master\'s Thesis, 2026): AI feedback analytics platform combining NPS tracking, sentiment analysis (Gemini Pro, RoBERTa), and consumer insight generation — distinction-grade. ', BODY),
            link('[View on GitHub]', 'https://github.com/Abiola97/All-Projects', BODY, MID_BLUE),
          ],
          spacing: { before:30, after:30 },
          indent: { left:160 },
        }),
        bullet('', 'Closing Nigeria\'s Flood Data Gap — Evidence-Based Policy Brief: Research synthesis applying collective intelligence frameworks to disaster response and energy/infrastructure resilience, demonstrating end-to-end research-to-policy translation.'),
        new Paragraph({
          children: [
            bold('▸ ', BODY, DARK_BLUE),
            normal('NLP Consumer Sentiment Analysis — RoBERTa Model: Applied NLP project classifying 10,000+ consumer product reviews, demonstrating advanced qualitative data analysis at scale. ', BODY),
            link('[View on GitHub]', 'https://github.com/Abiola97/All-Projects', BODY, MID_BLUE),
          ],
          spacing: { before:30, after:30 },
          indent: { left:160 },
        }),

        // ── EDUCATION ──
        sectionHeader('Education'),
        roleHeader("Master's in Collective Intelligence", '2024 – 2026'),
        companyLine('Mohammed VI Polytechnic University (UM6P)', 'Morocco · 75%, Mention Bien'),
        new Paragraph({
          children: [italic('Modules: Statistical Analysis & Research, Data Science, AI/ML, Experimental & Research Methods, MEL Studies, Behavioural Science, Organisational Leadership, Political Science, Project Management', SMALL, GREY)],
          spacing: { before:20, after:50 },
        }),

        roleHeader('B.Tech. Physics Electronics', '2013 – 2018'),
        companyLine('Federal University of Technology, Akure (FUTA)', 'Nigeria · Second Class Upper'),

        // ── CERTIFICATIONS ──
        sectionHeader('Certifications'),
        new Paragraph({
          children: [
            bold('▸ ', BODY, DARK_BLUE),
            link('Google Data Analytics Professional Certificate', 'https://www.coursera.org/professional-certificates/google-data-analytics', BODY),
            normal(' (Google & Coursera)', BODY, GREY),
            normal('   ', BODY),
            bold('▸ ', BODY, DARK_BLUE),
            link('Power BI for Business Intelligence', 'https://www.mygreatlearning.com/academy/learn-for-free/courses/power-bi', BODY),
            normal(' (Great Learning)', BODY, GREY),
          ],
          spacing: { before:40, after:20 },
        }),
        new Paragraph({
          children: [
            bold('▸ ', BODY, DARK_BLUE),
            link('Business Analysis with Excel', 'https://www.coursera.org/learn/business-analysis-excel', BODY),
            normal(' (Johns Hopkins University)', BODY, GREY),
            normal('   ', BODY),
            bold('▸ ', BODY, DARK_BLUE),
            link('Google Project Management Specialization', 'https://www.coursera.org/professional-certificates/google-project-management', BODY),
          ],
          spacing: { before:0, after:20 },
        }),
        new Paragraph({
          children: [
            bold('▸ ', BODY, DARK_BLUE),
            link('McKinsey Forward Learning Program', 'https://www.mckinsey.com/forward/overview', BODY),
            normal('   ', BODY),
            bold('▸ ', BODY, DARK_BLUE),
            link('Generative AI: Prompt Engineering', 'https://www.coursera.org/learn/generative-ai-prompt-engineering-for-everyone', BODY),
            normal(' (IBM)', BODY, GREY),
            normal('   ', BODY),
            bold('▸ ', BODY, DARK_BLUE),
            link('Data Analysis with R Programming', 'https://www.coursera.org/learn/data-analysis-r', BODY),
            normal(' (Coursera)', BODY, GREY),
          ],
          spacing: { before:0, after:40 },
        }),

        // ── PORTFOLIO LINKS ──
        sectionHeader('Portfolio & Profiles'),
        new Paragraph({
          children: [
            bold('LinkedIn: ', BODY),
            link('linkedin.com/in/abiola-ajao', 'https://www.linkedin.com/in/abiola-ajao', BODY),
            normal('  |  ', BODY, GREY),
            bold('GitHub: ', BODY),
            link('github.com/Abiola97/All-Projects', 'https://github.com/Abiola97/All-Projects', BODY),
            normal('  |  ', BODY, GREY),
            bold('Tableau: ', BODY),
            link('public.tableau.com/app/profile/ajao.abiola', 'https://public.tableau.com/app/profile/ajao.abiola', BODY),
          ],
          spacing: { before:40, after:40 },
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

  const outDir = process.argv[3] || '/mnt/user-data/outputs';
  const safeTitle = (job.title || 'Analyst').replace(/[^a-zA-Z0-9]/g, '_').substring(0, 30);
  const safeCompany = (job.company || 'Company').replace(/[^a-zA-Z0-9]/g, '_').substring(0, 20);
  const filename = `Ajao_Abiola_${safeTitle}_${safeCompany}_CV.docx`;
  const outPath = `${outDir}/${filename}`;

  const doc = buildCV(job);
  const buf = await Packer.toBuffer(doc);
  fs.writeFileSync(outPath, buf);
  console.log(outPath);
}

main().catch(e => { console.error(e); process.exit(1); });
