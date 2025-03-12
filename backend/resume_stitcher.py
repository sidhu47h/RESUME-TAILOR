def generate_header():
    """Generate the LaTeX header with document class and package imports."""
    return r"""\documentclass[letterpaper,10.5pt]{article}

\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage[usenames,dvipsnames]{color}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\usepackage{fontawesome5}
\usepackage{multicol}
\setlength{\multicolsep}{-3.0pt}
\setlength{\columnsep}{-1pt}
\input{glyphtounicode}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\addtolength{\oddsidemargin}{-0.6in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1.19in}
\addtolength{\topmargin}{-0.7in}
\addtolength{\textheight}{1.4in}

\urlstyle{same}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{
  \scshape\raggedright\large\bfseries
}{}{0em}{}[\color{black}\titlerule]

\pdfgentounicode=1

\newcommand{\resumeItem}[1]{%
  \item\small{#1}
}

\newcommand{\classesList}[4]{%
  \item\small{#1 #2 #3 #4}
}

\newcommand{\resumeSubheading}[4]{%
  \item
  \begin{tabular*}{1.0\textwidth}[t]{l@{\extracolsep{\fill}}r}
    \textbf{#1} & \textbf{\small #2} \\
    \textit{\small #3} & \textit{\small #4} \\
  \end{tabular*}
}

\newcommand{\resumeSubSubheading}[2]{%
  \item
  \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
    \textit{\small #1} & \textit{\small #2} \\
  \end{tabular*}
}

\newcommand{\resumeProjectHeading}[2]{%
  \item
  \begin{tabular*}{1.001\textwidth}{l@{\extracolsep{\fill}}r}
    \small #1 & \textbf{\small #2} \\
  \end{tabular*}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}}

\renewcommand\labelitemi{{$\vcenter{\hbox{\tiny$\bullet$}}$}}
\renewcommand\labelitemii{{$\vcenter{\hbox{\tiny$\bullet$}}$}}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.0in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}}

\begin{document}
"""

def generate_contact_section(resume):
    """Generate the contact information section."""
    name = resume.get("name", "")
    contact = resume.get("contact", {})
    
    contact_items = []
    if contact.get("phone"):
        contact_items.append(r"\raisebox{-0.1\height}\faPhone\ " + contact["phone"])
    if contact.get("email"):
        contact_items.append(r"\href{mailto:" + contact["email"] + r"}{\raisebox{-0.2\height}\faEnvelope\ " + contact["email"] + "}")
    if contact.get("linkedin"):
        linkedin_url = "https://" + contact["linkedin"] if not contact["linkedin"].startswith("http") else contact["linkedin"]
        contact_items.append(r"\href{" + linkedin_url + r"}{\raisebox{-0.2\height}\faLinkedin\ " + linkedin_url + "}")
    if contact.get("github"):
        github_url = "https://" + contact["github"] if not contact["github"].startswith("http") else contact["github"]
        contact_items.append(r"\href{" + github_url + r"}{\raisebox{-0.2\height}\faGithub\ " + github_url + "}")

    return r"""
\begin{center}
    {\Huge \scshape """ + name + r"""} \\ 
    \small """ + " ~ ".join(contact_items) + r"""
\end{center}
"""

def generate_about_section(resume):
    """Generate the about section."""
    about = resume.get("about", "")
    return r"""
\section{About}
{\fontsize{10pt}{10pt}\selectfont
""" + about + r"""
}
"""

def generate_skills_section(resume):
    """Generate the skills section."""
    skills = resume.get("skills", {})
    skills_items = []
    
    if "programmingLanguages" in skills:
        skills_items.append(r"\textbf{Programming Languages:} " + ", ".join(skills["programmingLanguages"]))
    if "frontEnd" in skills:
        skills_items.append(r"\textbf{Web Development:} " + ", ".join(skills["frontEnd"]))
    if "backEndFrameworks" in skills:
        skills_items.append(r"\textbf{Back-end Frameworks:} " + ", ".join(skills["backEndFrameworks"]))
    if "testing" in skills:
        skills_items.append(r"\textbf{Testing \& QA:} " + ", ".join(skills["testing"]))
    if "devOps" in skills:
        skills_items.append(r"\textbf{DevOps \& CI/CD:} " + ", ".join(skills["devOps"]))
    if "databases" in skills:
        skills_items.append(r"\textbf{Databases:} " + ", ".join(skills["databases"]))
    if "cloudTechnologies" in skills:
        skills_items.append(r"\textbf{Cloud Technologies:} " + ", ".join(skills["cloudTechnologies"]))
    if "additionalExpertise" in skills:
        skills_items.append(r"\textbf{Expertise:} " + ", ".join(skills["additionalExpertise"]))

    return r"""
\section{Skills}
\begin{itemize}[leftmargin=0.15in, label={}]
    \small\item{ """ + r' \\'.join(skills_items) + r""" }
\end{itemize}
"""

def generate_experience_section(resume):
    """Generate the experience section."""
    experiences = resume.get("experience", [])
    experience_items = []
    
    for exp in experiences:
        company = exp.get("company", "")
        period = exp.get("employmentPeriod", "")
        position = exp.get("position", "")
        location = exp.get("location", "")
        
        exp_str = r"\resumeSubheading" + "\n" + \
            f"      {{{company}}}{{{period}}}" + "\n" + \
            f"      {{{position}}}{{{location}}}" + "\n" + \
            r"      \resumeItemListStart"
        
        if "technologies" in exp:
            exp_str += "\n" + \
                r"          \resumeItem{\textbf{Technologies:} " + \
                ", ".join(exp['technologies']) + "}"
            
        for resp in exp.get("responsibilities", []):
            exp_str += "\n" + \
                r"          \resumeItem{" + resp + "}"
            
        exp_str += "\n" + \
            r"      \resumeItemListEnd"
        experience_items.append(exp_str)
    
    return r"""
\section{Experience}
\resumeSubHeadingListStart
""" + "\n".join(experience_items) + r"""
\resumeSubHeadingListEnd
"""

def generate_education_section(resume):
    """Generate the education section."""
    education = resume.get("education", [])
    education_items = []
    
    for edu in education:
        institution = edu.get("institution", "")
        period = edu.get("period", "")
        degree = edu.get("degree", "")
        location = edu.get("location", "")
        
        education_items.append(r"\resumeSubheading" + "\n" + \
            f"      {{{institution}}}{{{period}}}" + "\n" + \
            f"      {{{degree}}}{{{location}}}")
    
    return r"""
\section{Education}
\resumeSubHeadingListStart
""" + "\n".join(education_items) + r"""
\resumeSubHeadingListEnd
"""

def generate_projects_section(resume):
    """Generate the projects section."""
    projects = resume.get("projects", [])
    project_items = []
    
    for proj in projects:
        name = proj.get("name", "")
        date = proj.get("date", "")
        description = proj.get("description", "")
        technologies = proj.get("technologies", [])
        
        project_items.append(r"\resumeProjectHeading" + "\n" + \
            r"          {\textbf{" + name + r"} $|$ \emph{" + ", ".join(technologies) + r"}}{" + date + "}" + "\n" + \
            r"          \resumeItemListStart" + "\n" + \
            r"              \resumeItem{" + description + "}" + "\n" + \
            r"          \resumeItemListEnd")
    
    return r"""
\section{Projects}
\resumeSubHeadingListStart
""" + "\n".join(project_items) + r"""
\resumeSubHeadingListEnd
"""

def generate_additional_section(resume):
    """Generate the additional experiences and awards section."""
    additional = resume.get("additionalExperiencesAndAwards", [])
    if not additional:
        return ""
        
    items = "\n".join([r"\resumeItem{" + item + "}" for item in additional])
    
    return r"""
\section{Additional Experiences and Awards}
\resumeSubHeadingListStart
\resumeItemListStart
""" + items + r"""
\resumeItemListEnd
\resumeSubHeadingListEnd
"""

def generate_latex(resume):
    """Generate the complete LaTeX document from the resume JSON."""
    sections = [
        generate_header(),
        generate_contact_section(resume),
        generate_about_section(resume),
        generate_skills_section(resume),
        generate_experience_section(resume),
        generate_education_section(resume),
        generate_projects_section(resume),
        generate_additional_section(resume),
        r"\end{document}"
    ]
    
    return '\n'.join(sections)
