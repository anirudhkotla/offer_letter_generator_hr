# Role Definitions and Department Responsibilities
# This file serves as the template database for roles and snippets

ROLE_DEFINITIONS = {
    "Software Engineer": {
        "department": "Engineering",
        "reporting_to": "Engineering Manager",
        "key_areas": ["Backend Development", "Frontend Development", "Code Review", "System Design"],
    },
    "AI Intern": {
        "department": "AI/ML",
        "reporting_to": "AI Lead",
        "key_areas": ["Model Training", "Data Preprocessing", "Research", "Documentation"],
    },
    "Growth Marketing Executive": {
        "department": "Marketing",
        "reporting_to": "Marketing Director",
        "key_areas": ["Account-Based Marketing", "Social Media", "Content Strategy", "Analytics"],
    },
    "Product Manager": {
        "department": "Product",
        "reporting_to": "VP of Product",
        "key_areas": ["Roadmap Planning", "Stakeholder Management", "Market Research", "Agile Delivery"],
    },
    "Data Analyst": {
        "department": "Data",
        "reporting_to": "Data Lead",
        "key_areas": ["Data Visualization", "SQL Reporting", "Dashboard Creation", "Insights Generation"],
    },
    "Business Development Executive": {
        "department": "Sales",
        "reporting_to": "Sales Manager",
        "key_areas": ["Lead Generation", "Client Outreach", "Partnerships", "Revenue Growth"],
    },
    "HR Executive": {
        "department": "Human Resources",
        "reporting_to": "HR Manager",
        "key_areas": ["Recruitment", "Onboarding", "Employee Engagement", "Policy Compliance"],
    },
    "Other": {
        "department": "General",
        "reporting_to": "Director",
        "key_areas": [],
    },
}

GENERAL_EXPECTATIONS = [
    "Be an active contributor to Tericsoft's culture.",
    "Collaborate closely with other team members.",
    "Provide support in varied areas beyond the job description, as needed.",
]

INTERNSHIP_STATIC_INTRO = (
    "In reference to your application, we would like to congratulate you on your internship "
    "for the position of {role} for {duration}. Your internship is scheduled to start effective "
    "from {joining_date}. All of us at Tericsoft are excited that you will be joining our team."
)

INTERNSHIP_STATIC_BODY = (
    "As such, your internship will include training and focus primarily on learning and developing "
    "new skills and gaining a deeper understanding of {role_area}, working alongside {mentor}, "
    "assisting in day-to-day tasks and creating positive impact in the team. "
    "Based on your performance after {duration}, your employment will be rediscussed.\n\n"
    "The in-depth details of the internship will be shared by {mentor}."
)

FULLTIME_STATIC_INTRO = (
    "It gives us great pleasure to extend you an offer to join the Tericsoft Technology team! "
    "We would like you to join in the role of {role} reporting to {reporting_to}. "
    "We were impressed with your strong ability combined with your enthusiasm to support the "
    "development of Tericsoft's vision & mission. Together, we feel that these attributes will make "
    "you an outstanding fit as part of Tericsoft's technology team.\n\n"
    "This letter contains the relevant information regarding your offer."
)

FULLTIME_TERM_CLAUSE = (
    "As {role}, you will start on a {probation_period}-month probation period with the intention "
    "of extending into the permanent role. Your services will be confirmed in writing after the "
    "successful completion of your probation period. The probation period may be extended if your "
    "performance does not meet expectations."
)

FULLTIME_COMPENSATION_CLAUSE = (
    "We are pleased to offer you compensation including:\n\n"
    "Salary: You will receive a fixed salary of INR {monthly_salary}/- per month (Inclusive of all "
    "taxes & benefits). Your fixed CTC (Cost to Company) will be INR {ctc}/- per annum."
)

FULLTIME_CLOSING_CLAUSES = """Offer stands cancelled in case of any deviations in information/if not reported before the date of acceptance.

Please reply with your confirmation of acceptance of offer by {acceptance_deadline}. You will have to submit certain documents as a part of the onboarding process on the joining date.

Notice Period – During probation period, the notice period stands for 30 days. Post probation, the notice period stands for 60 days. You will be on probation for {probation_period} months from the date of your joining mentioned below.

Date of Joining: {joining_date}.

I am confident you will have a rewarding experience with a phenomenal team. We look forward to welcoming you to Tericsoft Technology."""

SIGNATURE_BLOCK = """Sincerely,

Abdul Rahman
Director
Tericsoft Technology"""

INTERNSHIP_ACCEPTANCE_BLOCK = "I accept the terms of this offer with Tericsoft.\n\n_____________________________________ Date -_______________________________________\n{full_name}"

FULLTIME_ACCEPTANCE_BLOCK = "I accept this action as outlined above and confirm with the above mentioned start date.\n\n_____________________________________ Date -_____________________________________\n{full_name}"
