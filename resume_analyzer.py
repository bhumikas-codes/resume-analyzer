name = input("Enter your name: ")

user_skills = input("Enter your skills separated by comma: ")
resume_skills = [skill.strip().lower() for skill in user_skills.split(",")]

role = input("Enter job role you are applying for: ").lower().strip()

job_skills_input = {
    "frontend developer": {
        "mandatory": {
            "all": ["html", "css", "javascript"],
            "one_of": ["react", "angular", "vue"]
        },

        "core": [
            "responsive design",
            "api integration",
            "git",
            "state management"
        ],

        "bonus": [
            "typescript",
            "next.js",
            "deployment"
        ]
        },
    

    "data analyst": {

    "mandatory": {
        "all": ["sql", "excel", "statistics"],
        "one_of": ["python", "r"]
    },

    "core": [
        "pandas",
        "numpy",
        "data cleaning",
        "data visualization",
        "exploratory data analysis"
    ],

    "bonus": [
        "power bi",
        "tableau",
        "a/b testing",
        "business intelligence"
    ]
},
 
    "backend developer": {

    "mandatory": {
        "all": ["sql", "rest api"],
        "one_of": ["python", "java", "node.js"]
    },

    "core": [
        "django",
        "flask",
        "spring boot",
        "express",
        "authentication",
        "database management"
    ],

    "bonus": [
        "docker",
        "aws",
        "redis",
        "microservices",
        "ci/cd"
    ]
},


     "full stack developer": {

    "mandatory": {
        "all": ["html", "css", "javascript", "sql", "rest api"],
        "one_of": ["python", "java", "node.js", "react", "angular", "vue"]
    },

    "core": [
        "frontend framework",
        "backend framework",
        "authentication",
        "git",
        "database integration"
    ],

    "bonus": [
        "docker",
        "aws",
        "deployment",
        "web security",
        "performance optimization"
    ]
},

 "machine learning engineer": {

    "mandatory": {
        "all": [
            "python",
            "machine learning",
            "linear algebra",
            "statistics"
        ],
        "one_of": ["scikit-learn", "tensorflow", "pytorch"]
    },

    "core": [
        "pandas",
        "numpy",
        "data preprocessing",
        "model evaluation",
        "feature engineering"
    ],

    "bonus": [
        "deep learning",
        "nlp",
        "computer vision",
        "mlops",
        "model deployment"
    ]
}

}


selected_role = job_skills_input.get(role)
if not selected_role:
    print("Invalid role entered.")
    exit()

mandatory_all = selected_role["mandatory"]["all"]
mandatory_one = selected_role["mandatory"]["one_of"]
all_match = all(skill in resume_skills for skill in mandatory_all)
one_match = any(skill in resume_skills for skill in mandatory_one)
if not all_match or not one_match:
    print("you do not meet mandatory requirements.")
    exit()

core_skills = selected_role["core"]
core_match_count = sum(skill in resume_skills for skill in core_skills)
core_percentage = core_match_count / len(core_skills)
print("core skills matched:", core_match_count)
print(" Core per", core_percentage)


bonus_skills = selected_role["bonus"]
bonus_match_count = sum(skill in resume_skills for skill in bonus_skills)
bonus_percentage = bonus_match_count/ len(bonus_skills)
print("Bonus skills matched:", bonus_match_count)
print("Bonus per:", bonus_percentage)

mandatory_score = 1
overall_score = (mandatory_score * 0.5) + (core_percentage * 0.3) + (bonus_percentage * 0.2)
print("Overall readiness score is:", overall_score)
score_percent = overall_score * 100
print("Overall readiness score:", round(score_percent, 2), "%")


if score_percent >= 75:
    print("You're highly ready for this role.")
elif score_percent >= 30:
    print("You're fairly prepared but improving a few core skills will help!.")
else:
    print("You need to build more skills before applying.")


