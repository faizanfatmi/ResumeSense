"""
Keyword Analyzer — Extracts and categorizes keywords from documents.
"""
import re
import logging
from collections import Counter
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# Technical skills database
TECHNICAL_SKILLS = {
    # Programming Languages
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c', 'ruby', 'go', 'golang',
    'rust', 'swift', 'kotlin', 'php', 'scala', 'r', 'matlab', 'perl', 'dart', 'lua',
    'objective-c', 'assembly', 'bash', 'shell', 'powershell', 'vba',

    # Web Technologies
    'html', 'html5', 'css', 'css3', 'sass', 'scss', 'less', 'tailwind', 'bootstrap',
    'react', 'reactjs', 'react.js', 'angular', 'angularjs', 'vue', 'vuejs', 'vue.js',
    'next.js', 'nextjs', 'nuxt', 'nuxtjs', 'svelte', 'jquery', 'webpack', 'vite',
    'node.js', 'nodejs', 'express', 'express.js', 'django', 'flask', 'fastapi',
    'spring', 'spring boot', 'asp.net', '.net', 'laravel', 'rails', 'ruby on rails',

    # Data Science / ML
    'machine learning', 'deep learning', 'artificial intelligence', 'ai', 'ml',
    'natural language processing', 'nlp', 'computer vision', 'neural network',
    'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'sklearn', 'pandas', 'numpy',
    'scipy', 'matplotlib', 'seaborn', 'plotly', 'opencv', 'spacy', 'nltk',
    'hugging face', 'transformers', 'bert', 'gpt', 'llm', 'rag',
    'data science', 'data analysis', 'data engineering', 'data mining',
    'data visualization', 'statistics', 'statistical analysis',
    'regression', 'classification', 'clustering', 'random forest',
    'xgboost', 'gradient boosting', 'decision tree', 'svm',
    'feature engineering', 'model training', 'model deployment',

    # Databases
    'sql', 'mysql', 'postgresql', 'postgres', 'mongodb', 'redis', 'elasticsearch',
    'cassandra', 'dynamodb', 'firebase', 'firestore', 'sqlite', 'oracle',
    'microsoft sql server', 'mssql', 'mariadb', 'neo4j', 'couchdb',
    'nosql', 'graphql',

    # Cloud & DevOps
    'aws', 'amazon web services', 'azure', 'microsoft azure', 'gcp',
    'google cloud', 'google cloud platform', 'heroku', 'vercel', 'netlify',
    'docker', 'kubernetes', 'k8s', 'terraform', 'ansible', 'jenkins',
    'ci/cd', 'github actions', 'gitlab ci', 'circleci', 'travis ci',
    'nginx', 'apache', 'linux', 'unix', 'ubuntu',

    # Tools
    'git', 'github', 'gitlab', 'bitbucket', 'svn', 'jira', 'confluence',
    'slack', 'trello', 'asana', 'notion', 'figma', 'sketch', 'adobe xd',
    'photoshop', 'illustrator', 'canva', 'tableau', 'power bi', 'looker',
    'excel', 'google sheets', 'jupyter', 'jupyter notebook', 'colab',
    'vs code', 'visual studio', 'intellij', 'pycharm', 'eclipse',
    'postman', 'swagger', 'rest api', 'restful', 'api', 'microservices',
    'agile', 'scrum', 'kanban',

    # Mobile
    'android', 'ios', 'react native', 'flutter', 'xamarin', 'ionic',
    'swift ui', 'swiftui', 'jetpack compose',

    # Other
    'blockchain', 'ethereum', 'solidity', 'web3',
    'cybersecurity', 'penetration testing', 'encryption',
    'iot', 'embedded systems', 'raspberry pi', 'arduino',
    'unity', 'unreal engine', 'game development',
}

SOFT_SKILLS = {
    'communication', 'leadership', 'teamwork', 'problem solving', 'problem-solving',
    'critical thinking', 'creativity', 'adaptability', 'time management',
    'project management', 'collaboration', 'interpersonal', 'presentation',
    'negotiation', 'conflict resolution', 'mentoring', 'coaching',
    'strategic thinking', 'decision making', 'analytical', 'attention to detail',
    'multitasking', 'self-motivated', 'initiative', 'flexibility',
    'work ethic', 'organizational', 'planning', 'prioritization',
    'customer service', 'client relations', 'stakeholder management',
    'public speaking', 'written communication', 'verbal communication',
    'emotional intelligence', 'cultural awareness', 'cross-functional',
    'team building', 'result-oriented', 'goal-oriented',
}

TOOLS_AND_PLATFORMS = {
    'microsoft office', 'ms office', 'word', 'powerpoint', 'outlook',
    'google workspace', 'google docs', 'google drive',
    'salesforce', 'hubspot', 'zendesk', 'freshdesk',
    'sap', 'oracle erp', 'workday',
    'autocad', 'solidworks', 'matlab', 'simulink',
    'spss', 'stata', 'sas',
}


@dataclass
class KeywordAnalysisResult:
    technical_skills: list = field(default_factory=list)
    soft_skills: list = field(default_factory=list)
    tools: list = field(default_factory=list)
    all_keywords: list = field(default_factory=list)
    keyword_density: float = 0.0
    keyword_score: float = 0.0
    issues: list = field(default_factory=list)


def analyze_keywords(text: str) -> KeywordAnalysisResult:
    """Extract and categorize keywords from document text."""
    result = KeywordAnalysisResult()

    if not text or len(text.strip()) < 10:
        result.keyword_score = 0
        return result

    text_lower = text.lower()

    # Find technical skills
    found_technical = []
    for skill in TECHNICAL_SKILLS:
        # Use word boundary matching for short terms
        if len(skill) <= 3:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_technical.append(skill.upper() if len(skill) <= 3 else skill.title())
        else:
            if skill in text_lower:
                found_technical.append(skill.title())

    result.technical_skills = sorted(set(found_technical))

    # Find soft skills
    found_soft = []
    for skill in SOFT_SKILLS:
        if skill in text_lower:
            found_soft.append(skill.title())
    result.soft_skills = sorted(set(found_soft))

    # Find tools
    found_tools = []
    for tool in TOOLS_AND_PLATFORMS:
        if tool in text_lower:
            found_tools.append(tool.title())
    result.tools = sorted(set(found_tools))

    # All keywords combined
    result.all_keywords = result.technical_skills + result.soft_skills + result.tools

    # Calculate keyword density
    word_count = len(text.split())
    keyword_count = len(result.all_keywords)
    result.keyword_density = (keyword_count / word_count * 100) if word_count > 0 else 0

    # Calculate keyword score
    result.keyword_score = calculate_keyword_score(result)

    # Generate issues
    if len(result.technical_skills) == 0:
        result.issues.append({
            'severity': 'critical',
            'title': 'No technical skills detected',
            'description': 'No recognizable technical skills were found in the document.',
            'recommendation': 'Add relevant technical skills that accurately describe your capabilities.',
        })
    elif len(result.technical_skills) < 5:
        result.issues.append({
            'severity': 'important',
            'title': 'Few technical skills detected',
            'description': f'Only {len(result.technical_skills)} technical skills were identified.',
            'recommendation': 'Consider adding more specific technical skills relevant to your target role.',
        })
    else:
        result.issues.append({
            'severity': 'good',
            'title': f'{len(result.technical_skills)} technical skills detected',
            'description': 'A solid set of technical skills was found in the document.',
        })

    if len(result.soft_skills) == 0:
        result.issues.append({
            'severity': 'suggestion',
            'title': 'No soft skills detected',
            'description': 'No recognizable soft skills were found.',
            'recommendation': 'Consider mentioning relevant soft skills like communication, leadership, or teamwork.',
        })

    return result


def calculate_keyword_score(result: KeywordAnalysisResult) -> float:
    """Calculate keyword coverage score."""
    score = 0

    # Technical skills (up to 50 points)
    tech_count = len(result.technical_skills)
    if tech_count >= 10:
        score += 50
    elif tech_count >= 5:
        score += 35
    elif tech_count >= 3:
        score += 25
    elif tech_count >= 1:
        score += 15

    # Soft skills (up to 25 points)
    soft_count = len(result.soft_skills)
    if soft_count >= 5:
        score += 25
    elif soft_count >= 3:
        score += 20
    elif soft_count >= 1:
        score += 10

    # Tools (up to 25 points)
    tool_count = len(result.tools)
    if tool_count >= 3:
        score += 25
    elif tool_count >= 1:
        score += 15

    return min(100, score)
