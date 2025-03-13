def generate_latex(data):
    def escape_latex(text):
        """
        Escape LaTeX-sensitive characters in text.
        """
        if not isinstance(text, str):
            return text
        replacements = {
            '\\': r'\textbackslash{}',
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}'
        }
        for char, repl in replacements.items():
            text = text.replace(char, repl)
        return text

    # ------------------ Header (Contact and Name) ------------------
    header = []
    header.append(r"\begin{center}")
    name = escape_latex(data.get("name", ""))
    header.append(f"    {{\\Huge \\scshape {name}}} \\\\")
    contact = data.get("contact", {})
    phone = escape_latex(contact.get("phone", ""))
    email = escape_latex(contact.get("email", ""))
    linkedin = escape_latex(contact.get("linkedin", ""))
    github = escape_latex(contact.get("github", ""))
    # If not provided as a URL, prepend protocol.
    linkedin_url = linkedin if linkedin.startswith("http") else "https://" + linkedin
    github_url = github if github.startswith("http") else "https://" + github
    header.append(f"    \\small \\raisebox{{-0.1\\height}}\\faPhone\\ {phone} ~ ")
    header.append(f"    \\href{{mailto:{email}}}{{\\raisebox{{-0.2\\height}}\\faEnvelope\\ {email}}} ~")
    header.append(f"    \\href{{{linkedin_url}}}{{\\raisebox{{-0.2\\height}}\\faLinkedin\\ {linkedin_url}}} ~")
    header.append(f"    \\href{{{github_url}}}{{\\raisebox{{-0.2\\height}}\\faGithub\\ {github_url}}}")
    header.append(r"\end{center}")
    header.append("")  # Blank line after header

    # ------------------ About Section ------------------
    about_section = []
    about_section.append(r"\section{About}")
    about_text = escape_latex(data.get("about", ""))
    about_section.append(r"{\fontsize{10pt}{10pt}\selectfont")
    about_section.append(f"{about_text}")
    about_section.append("}")
    about_section.append("")

    # ------------------ Skills Section ------------------
    skills_section = []
    skills_section.append(r"\section{Skills}")
    skills_section.append(r"\begin{itemize}[leftmargin=0.15in, label={}]")
    # We create one item containing a block of skills.
    skills_section.append(r"    \small\item{ ")
    # Define the mapping (key in JSON -> label to show)
    skills_mapping = [
        ("programmingLanguages", "Programming Languages"),
        ("backEndFrameworks", "Back-end Frameworks"),
        ("frontEnd", "Front-end"),
        ("testing", "Testing \& QA"),
        ("devOps", "DevOps \& CI/CD"),
        ("databases", "Databases"),
        ("cloudTechnologies", "Cloud Technologies"),
        ("additionalExpertise", "Expertise")
    ]
    skill_lines = []
    for key, label in skills_mapping:
        items = data.get("skills", {}).get(key, [])
        if items:
            # Escape each item in the list.
            escaped_items = [escape_latex(item) for item in items]
            line = f"\\textbf{{{label}:}} " + ", ".join(escaped_items)
            skill_lines.append(line)
    # Join the lines with LaTeX line breaks.
    skills_section.append(" \\\\ ".join(skill_lines) + " }")
    skills_section.append(r"\end{itemize}")
    skills_section.append("")

    # ------------------ Experience Section ------------------
    experience_section = []
    experience_section.append(r"\section{Experience}")
    experience_section.append(r"\resumeSubHeadingListStart")
    experiences = data.get("experience", [])
    for exp in experiences:
        company = escape_latex(exp.get("company", ""))
        period = escape_latex(exp.get("employmentPeriod", ""))
        position = escape_latex(exp.get("position", ""))
        location = escape_latex(exp.get("location", "")) if exp.get("location") else ""
        experience_section.append(r"\resumeSubheading")
        experience_section.append(f"      {{{company}}}{{{period}}}")
        experience_section.append(f"      {{{position}}}{{{location}}}")
        experience_section.append(r"      \resumeItemListStart")
        # First line: list the technologies used (if available).
        technologies = exp.get("technologies", [])
        if technologies:
            escaped_tech = [escape_latex(tech) for tech in technologies]
            tech_line = "\\textbf{Technologies:} " + ", ".join(escaped_tech)
            experience_section.append(f"          \\resumeItem{{{tech_line}}}")
        # List each responsibility.
        for resp in exp.get("responsibilities", []):
            experience_section.append(f"          \\resumeItem{{{escape_latex(resp)}}}")
        experience_section.append(r"      \resumeItemListEnd")
    experience_section.append(r"\resumeSubHeadingListEnd")
    experience_section.append("")

    # ------------------ Education Section ------------------
    education_section = []
    education_section.append(r"\section{Education}")
    education_section.append(r"\resumeSubHeadingListStart")
    for edu in data.get("education", []):
        institution = escape_latex(edu.get("institution", ""))
        # Replace unicode dash with LaTeX-friendly --
        period = escape_latex(edu.get("period", "").replace("\u2013", "--"))
        degree = escape_latex(edu.get("degree", ""))
        location = escape_latex(edu.get("location", ""))
        education_section.append(r"\resumeSubheading")
        education_section.append(f"      {{{institution}}}{{{period}}}")
        education_section.append(f"      {{{degree}}}{{{location}}}")
    education_section.append(r"\resumeSubHeadingListEnd")
    education_section.append("")

    # ------------------ Projects Section ------------------
    projects_section = []
    projects_section.append(r"\section{Projects}")
    projects_section.append(r"\resumeSubHeadingListStart")
    for proj in data.get("projects", []):
        proj_name = escape_latex(proj.get("name", ""))
        proj_date = escape_latex(proj.get("date", ""))
        proj_description = escape_latex(proj.get("description", ""))
        proj_tech = proj.get("technologies", [])
        if proj_tech:
            escaped_proj_tech = [escape_latex(t) for t in proj_tech]
            tech_str = ", ".join(escaped_proj_tech)
        else:
            tech_str = ""
        projects_section.append(r"\resumeProjectHeading")
        projects_section.append(f"          {{\\textbf{{{proj_name}}} $|$ \\emph{{{tech_str}}}}}{{{proj_date}}}")
        projects_section.append(r"          \resumeItemListStart")
        projects_section.append(f"              \\resumeItem{{{proj_description}}}")
        projects_section.append(r"          \resumeItemListEnd")
    projects_section.append(r"\resumeSubHeadingListEnd")
    projects_section.append("")

    # ------------------ Additional Experiences and Awards ------------------
    additional_section = []
    additional_section.append(r"\section{Additional Experiences and Awards}")
    additional_section.append(r"\resumeSubHeadingListStart")
    additional_section.append(r"\resumeItemListStart")
    for item in data.get("additionalExperiencesAndAwards", []):
        additional_section.append(f"\\resumeItem{{{escape_latex(item)}}}")
    additional_section.append(r"\resumeItemListEnd")
    additional_section.append(r"\resumeSubHeadingListEnd")
    additional_section.append("")

    # ------------------ Combine Everything into the Full Document ------------------
    lines = []
    lines.append(r"\documentclass[letterpaper,10.5pt]{article}")
    lines.append("")
    lines.append(r"\usepackage[empty]{fullpage}")
    lines.append(r"\usepackage{titlesec}")
    lines.append(r"\usepackage[usenames,dvipsnames]{color}")
    lines.append(r"\usepackage{enumitem}")
    lines.append(r"\usepackage[hidelinks]{hyperref}")
    lines.append(r"\usepackage{fancyhdr}")
    lines.append(r"\usepackage[english]{babel}")
    lines.append(r"\usepackage{tabularx}")
    lines.append(r"\usepackage{fontawesome5}")
    lines.append(r"\usepackage{multicol}")
    lines.append(r"\setlength{\multicolsep}{-3.0pt}")
    lines.append(r"\setlength{\columnsep}{-1pt}")
    lines.append(r"\input{glyphtounicode}")
    lines.append("")
    lines.append(r"\pagestyle{fancy}")
    lines.append(r"\fancyhf{}")
    lines.append(r"\fancyfoot{}")
    lines.append(r"\renewcommand{\headrulewidth}{0pt}")
    lines.append(r"\renewcommand{\footrulewidth}{0pt}")
    lines.append("")
    lines.append(r"\addtolength{\oddsidemargin}{-0.6in}")
    lines.append(r"\addtolength{\evensidemargin}{-0.5in}")
    lines.append(r"\addtolength{\textwidth}{1.19in}")
    lines.append(r"\addtolength{\topmargin}{-0.7in}")
    lines.append(r"\addtolength{\textheight}{1.4in}")
    lines.append("")
    lines.append(r"\urlstyle{same}")
    lines.append(r"\raggedbottom")
    lines.append(r"\raggedright")
    lines.append(r"\setlength{\tabcolsep}{0in}")
    lines.append("")
    lines.append(r"\titleformat{\section}{")
    lines.append(r"  \scshape\raggedright\large\bfseries")
    lines.append(r"}{}{0em}{}[\color{black}\titlerule]")
    lines.append("")
    lines.append(r"\pdfgentounicode=1")
    lines.append("")
    lines.append(r"\newcommand{\resumeItem}[1]{%")
    lines.append(r"  \item\small{#1}")
    lines.append(r"}")
    lines.append("")
    lines.append(r"\newcommand{\classesList}[4]{%")
    lines.append(r"  \item\small{#1 #2 #3 #4}")
    lines.append(r"}")
    lines.append("")
    lines.append(r"\newcommand{\resumeSubheading}[4]{%")
    lines.append(r"  \item")
    lines.append(r"  \begin{tabular*}{1.0\textwidth}[t]{l@{\extracolsep{\fill}}r}")
    lines.append(r"    \textbf{#1} & \textbf{\small #2} \\")
    lines.append(r"    \textit{\small #3} & \textit{\small #4} \\")
    lines.append(r"  \end{tabular*}")
    lines.append(r"}")
    lines.append("")
    lines.append(r"\newcommand{\resumeSubSubheading}[2]{%")
    lines.append(r"  \item")
    lines.append(r"  \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}")
    lines.append(r"    \textit{\small #1} & \textit{\small #2} \\")
    lines.append(r"  \end{tabular*}")
    lines.append(r"}")
    lines.append("")
    lines.append(r"\newcommand{\resumeProjectHeading}[2]{%")
    lines.append(r"  \item")
    lines.append(r"  \begin{tabular*}{1.001\textwidth}{l@{\extracolsep{\fill}}r}")
    lines.append(r"    \small #1 & \textbf{\small #2} \\")
    lines.append(r"  \end{tabular*}")
    lines.append(r"}")
    lines.append("")
    lines.append(r"\newcommand{\resumeSubItem}[1]{\resumeItem{#1}}")
    lines.append("")
    lines.append(r"\renewcommand\labelitemi{{$\vcenter{\hbox{\tiny$\bullet$}}$}}")
    lines.append(r"\renewcommand\labelitemii{{$\vcenter{\hbox{\tiny$\bullet$}}$}}")
    lines.append("")
    lines.append(r"\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.0in, label={}]}")
    lines.append(r"\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}")
    lines.append(r"\newcommand{\resumeItemListStart}{\begin{itemize}}")
    lines.append(r"\newcommand{\resumeItemListEnd}{\end{itemize}}")
    lines.append("")
    lines.append(r"\begin{document}")
    lines.append("")
    
    # Append all sections in order
    lines.extend(header)
    lines.extend(about_section)
    lines.extend(skills_section)
    lines.extend(experience_section)
    lines.extend(education_section)
    lines.extend(projects_section)
    lines.extend(additional_section)
    lines.append(r"\end{document}")
    
    return "\n".join(lines)