from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import sqlite3
from mcp.server.fastmcp import FastMCP
import json
from github import Github
import re
from pathlib import Path
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# GitHub API 토큰 설정
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
github = Github(GITHUB_TOKEN)

# 프로젝트 정보를 위한 Pydantic 모델
class ProjectMember(BaseModel):
    name: str
    role: str
    contributions: List[str]

class Project(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    tech_stack: List[str]
    members: List[ProjectMember]
    github_url: Optional[str] = None
    deployment_url: Optional[str] = None
    key_features: List[str]
    challenges: List[str]
    solutions: List[str]

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d['start_date'] = d['start_date'].isoformat()
        d['end_date'] = d['end_date'].isoformat()
        return d

# MCP 서버 인스턴스 생성
mcp = FastMCP("SSAFY Project Portfolio Server")

def load_template() -> dict:
    """Load the project information template."""
    with open('project_info_template.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def init_db():
    """데이터베이스 초기화"""
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    
    # 기존 테이블들 삭제
    cursor.execute("DROP TABLE IF EXISTS projects")
    cursor.execute("DROP TABLE IF EXISTS basic_info")
    cursor.execute("DROP TABLE IF EXISTS technical_info")
    cursor.execute("DROP TABLE IF EXISTS architecture_info")
    cursor.execute("DROP TABLE IF EXISTS code_quality")
    cursor.execute("DROP TABLE IF EXISTS portfolio_goals")
    cursor.execute("DROP TABLE IF EXISTS github_info")
    cursor.execute("DROP TABLE IF EXISTS refactoring_status")
    cursor.execute("DROP TABLE IF EXISTS documentation_status")
    
    # 프로젝트 기본 테이블
    cursor.execute('''
    CREATE TABLE projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 기본 정보 테이블
    cursor.execute('''
    CREATE TABLE basic_info (
        project_id INTEGER PRIMARY KEY,
        project_name TEXT,
        duration TEXT,
        team_size TEXT,
        your_role TEXT,
        main_objectives TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    ''')
    
    # 기술 정보 테이블
    cursor.execute('''
    CREATE TABLE technical_info (
        project_id INTEGER PRIMARY KEY,
        frontend_tech TEXT,
        backend_tech TEXT,
        database TEXT,
        deployment TEXT,
        other_tools TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    ''')
    
    # 아키텍처 정보 테이블
    cursor.execute('''
    CREATE TABLE architecture_info (
        project_id INTEGER PRIMARY KEY,
        current_structure TEXT,
        pain_points TEXT,
        desired_improvements TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    ''')
    
    # 코드 품질 테이블
    cursor.execute('''
    CREATE TABLE code_quality (
        project_id INTEGER PRIMARY KEY,
        debug_code TEXT,
        duplications TEXT,
        performance TEXT,
        readability TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    ''')
    
    # 포트폴리오 목표 테이블
    cursor.execute('''
    CREATE TABLE portfolio_goals (
        project_id INTEGER PRIMARY KEY,
        target_audience TEXT,
        key_highlights TEXT,
        personal_contributions TEXT,
        unique_selling_points TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    ''')
    
    # GitHub 정보 테이블
    cursor.execute('''
    CREATE TABLE github_info (
        project_id INTEGER PRIMARY KEY,
        repository_url TEXT,
        branch_structure TEXT,
        contribution_stats TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    ''')
    
    # 리팩토링 상태 테이블
    cursor.execute('''
    CREATE TABLE refactoring_status (
        project_id INTEGER PRIMARY KEY,
        completed_tasks TEXT,
        pending_tasks TEXT,
        skipped_tasks TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    ''')
    
    # 문서화 상태 테이블
    cursor.execute('''
    CREATE TABLE documentation_status (
        project_id INTEGER PRIMARY KEY,
        readme_generated BOOLEAN,
        created_at TIMESTAMP,
        last_updated TIMESTAMP,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    ''')
    
    conn.commit()
    conn.close()

def update_project_info(project_id, section, data):
    """프로젝트 정보 업데이트"""
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    
    # 섹션별 테이블 업데이트
    if section == "basicInfo":
        cursor.execute('''
        INSERT OR REPLACE INTO basic_info 
        (project_id, project_name, duration, team_size, your_role, main_objectives)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            project_id,
            data.get('projectName', ''),
            data.get('duration', ''),
            data.get('teamSize', ''),
            data.get('yourRole', ''),
            json.dumps(data.get('mainObjectives', []))
        ))
    
    elif section == "technicalInfo":
        cursor.execute('''
        INSERT OR REPLACE INTO technical_info 
        (project_id, frontend_tech, backend_tech, database, deployment, other_tools)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            project_id,
            json.dumps(data.get('frontendTech', [])),
            json.dumps(data.get('backendTech', [])),
            json.dumps(data.get('database', [])),
            json.dumps(data.get('deployment', [])),
            json.dumps(data.get('otherTools', []))
        ))
    
    # ... 다른 섹션들에 대한 업데이트 로직 추가 ...
    
    # 프로젝트 업데이트 시간 갱신
    cursor.execute('''
    UPDATE projects 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = ?
    ''', (project_id,))
    
    conn.commit()
    conn.close()

def get_project_info(project_id):
    """프로젝트 정보 조회"""
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    
    # 모든 섹션의 정보를 조회
    project_info = {}
    
    # 기본 정보 조회
    cursor.execute('SELECT * FROM basic_info WHERE project_id = ?', (project_id,))
    basic_info = cursor.fetchone()
    if basic_info:
        project_info['basicInfo'] = {
            'projectName': basic_info[1],
            'duration': basic_info[2],
            'teamSize': basic_info[3],
            'yourRole': basic_info[4],
            'mainObjectives': json.loads(basic_info[5])
        }
    
    # 기술 정보 조회
    cursor.execute('SELECT * FROM technical_info WHERE project_id = ?', (project_id,))
    tech_info = cursor.fetchone()
    if tech_info:
        project_info['technicalInfo'] = {
            'frontendTech': json.loads(tech_info[1]),
            'backendTech': json.loads(tech_info[2]),
            'database': json.loads(tech_info[3]),
            'deployment': json.loads(tech_info[4]),
            'otherTools': json.loads(tech_info[5])
        }
    
    # ... 다른 섹션들에 대한 조회 로직 추가 ...
    
    conn.close()
    return project_info

# POTLESS 프로젝트 정보 초기화
def init_potless_project():
    project_data = {
        'projectInfo': {
            'basicInfo': {
                'projectName': 'POTLESS',
                'duration': '2024-04-08 ~ 2024-05-20',
                'teamSize': '6명',
                'yourRole': '팀장, 모바일 개발자, AI/ML 엔지니어',
                'mainObjectives': [
                    'AI 기반 포트홀 자동 탐지 시스템 개발',
                    '구청 직원들의 실제 피드백을 반영한 기능 구현',
                    '모바일 환경에 최적화된 AI 모델 개발'
                ]
            },
            'technicalInfo': {
                'frontendTech': ['Flutter', 'Dart'],
                'backendTech': ['Python'],
                'database': [],
                'deployment': [],
                'otherTools': ['TensorFlow/PyTorch', 'Jupyter Notebook', 'Tesla V100 GPU']
            },
            'architectureInfo': {
                'currentStructure': '마이크로서비스 아키텍처',
                'painPoints': ['AI 모델 통합, 특히 On-Device AI 구현'],
                'desiredImprovements': []
            },
            'performance': {
                'async_processing': {
                    'isolate_parallel': {
                        'description': 'Isolate를 활용한 병렬 처리',
                        'details': '촬영-감지-업로드 작업을 각각 다른 isolate에 할당하여 처리'
                    }
                },
                'ai_optimization': {
                    'model_lightweight': {
                        'description': 'AI 모델 경량화',
                        'details': '모바일 환경에 적합한 모델 경량화 진행'
                    }
                }
            },
            'ai_development': {
                'hyperparameter_tuning': {
                    'description': '하이퍼파라미터 튜닝',
                    'details': 'batch-epoch 수준의 기본적인 튜닝 진행'
                },
                'dataset_preprocessing': {
                    'description': '데이터셋 전처리',
                    'details': '포트홀 인식 개선을 위한 데이터셋 전처리 중점'
                }
            },
            'project_management': {
                'methodology': {
                    'type': '애자일/스크럼',
                    'details': {
                        'sprint_meeting': '매주 월요일 스프린트 회의를 통한 주간 작업 계획 수립',
                        'daily_scrum': '매일 스크럼을 통한 상황 공유',
                        'user_feedback': '구청 직원들과의 정기적인 인터뷰를 통한 피드백 수집 및 반영'
                    }
                },
                'feedback_cycle': {
                    'description': '사용자 중심 피드백 사이클',
                    'details': '각 인터뷰를 데드라인으로 설정하고, 개발 후 피드백을 받아 지속적인 개선 진행'
                }
            },
            'collaboration_tools': {
                'project_management': {
                    'jira': {
                        'description': '프로젝트 관리 및 이슈 트래킹',
                        'usage': '스프린트 계획 및 작업 관리'
                    }
                },
                'version_control': {
                    'github': {
                        'description': '코드 버전 관리',
                        'usage': '소스 코드 관리 및 협업'
                    }
                },
                'documentation': {
                    'notion': {
                        'description': '문서화 및 지식 공유',
                        'usage': '프로젝트 문서 및 회의록 관리'
                    }
                },
                'design': {
                    'figma': {
                        'description': 'UI/UX 디자인',
                        'usage': '인터페이스 디자인 및 프로토타이핑'
                    }
                },
                'communication': {
                    'mattermost': {
                        'description': '팀 커뮤니케이션',
                        'usage': '일일 소통 및 정보 공유'
                    }
                }
            },
            'achievements': {
                'technical_achievements': {
                    'automation': {
                        'description': '포트홀 자동 탐지 시스템',
                        'details': 'AI 기반 자동 탐지 및 관리 서비스 구현'
                    },
                    'user_centric': {
                        'description': '사용자 중심 기능 개발',
                        'details': '구청 직원들의 실제 피드백을 반영한 기능 구현'
                    }
                },
                'project_quality': {
                    'completion': {
                        'description': '높은 완성도',
                        'details': '기술적, 기능적 측면에서 높은 완성도 달성'
                    }
                },
                'awards': {
                    'ssafy_competition': {
                        'description': 'SSAFY 10기 자율 프로젝트 결선 발표회',
                        'achievement': '전국 1등',
                        'details': '전국 SSAFY 캠퍼스 중 최우수 프로젝트 선정'
                    }
                }
            },
            'personal_growth': {
                'overall_growth': {
                    'description': '전반적인 역량 향상',
                    'areas': {
                        'technical': 'AI 모델 개발 및 모바일 앱 개발 역량',
                        'leadership': '팀장으로서의 리더십',
                        'problem_solving': '기술적 문제 해결 능력',
                        'communication': '팀원 및 이해관계자와의 커뮤니케이션',
                        'project_management': '애자일 방식의 프로젝트 관리'
                    }
                }
            }
        },
        'timestamp': {
            'created': datetime.now().isoformat(),
            'lastUpdated': datetime.now().isoformat()
        }
    }
    
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO projects (project_data) VALUES (?)", (json.dumps(project_data),))
    conn.commit()
    conn.close()

# 데이터베이스 초기화 및 POTLESS 프로젝트 정보 생성
init_db()
init_potless_project()

def extract_tech_stack(repo) -> List[str]:
    """레포지토리에서 기술 스택을 추출합니다."""
    tech_stack = set()
    
    # 1. 언어 정보에서 추출
    languages = repo.get_languages()
    tech_stack.update(languages.keys())
    
    # 2. README에서 기술 스택 추출
    try:
        readme = repo.get_readme()
        content = readme.decoded_content.decode('utf-8').lower()
        
        # 일반적인 기술 스택 섹션 패턴
        stack_patterns = [
            r"tech stack[:\s]*(.*?)(?=##|\Z)",
            r"기술 스택[:\s]*(.*?)(?=##|\Z)",
            r"사용 기술[:\s]*(.*?)(?=##|\Z)",
            r"technologies[:\s]*(.*?)(?=##|\Z)"
        ]
        
        for pattern in stack_patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                # 기술 스택 텍스트에서 일반적인 기술 키워드 추출
                tech_keywords = re.findall(r'`([^`]+)`|\*\*([^\*]+)\*\*|#\s*([^\n]+)|\b(react|vue|angular|node|python|java|spring|django|flask|mysql|postgresql|mongodb)\b', match.group(1), re.IGNORECASE)
                for keyword_groups in tech_keywords:
                    keyword = next((k for k in keyword_groups if k), None)
                    if keyword:
                        tech_stack.add(keyword.strip())
    except:
        pass
    
    return list(tech_stack)

def extract_features_and_challenges(repo) -> tuple[List[str], List[str], List[str]]:
    """레포지토리의 README에서 주요 기능과 도전 과제를 추출합니다."""
    features = []
    challenges = []
    solutions = []
    
    try:
        readme = repo.get_readme()
        content = readme.decoded_content.decode('utf-8')
        
        # 주요 기능 추출
        feature_section = re.search(r'# 📕주요기능[^\n]*\n(.*?)(?=\n#|\Z)', content, re.IGNORECASE | re.DOTALL)
        if feature_section:
            section_text = feature_section.group(1)
            # 번호가 매겨진 주요 기능 섹션 찾기
            numbered_sections = re.finditer(r'###\s*(\d+)\.\s*([^\n]+)', section_text)
            for section in numbered_sections:
                section_title = section.group(2)
                # 섹션 시작부터 다음 섹션이나 파일 끝까지의 내용 추출
                section_content = section_text[section.end():].split('###')[0]
                # 글머리 기호로 시작하는 상세 기능 추출
                details = re.findall(r'[-\*]\s*([^\n]+)', section_content)
                if details:
                    features.append(f"{section_title}: {', '.join(details)}")
                else:
                    features.append(section_title)
        
        # 기획 배경 및 도전 과제 추출
        challenge_patterns = [
            r"# 🔎기획배경\s*(.*?)(?=\n#|\Z)",
            r"문제[:\s]*(.*?)(?=##|\Z)",
            r"도전 과제[:\s]*(.*?)(?=##|\Z)"
        ]
        
        for pattern in challenge_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                challenge_text = match.group(1)
                # 글머리 기호로 시작하는 항목 추출
                items = re.findall(r'[-\*]\s*([^\n]+)', challenge_text)
                if items:
                    for item in items:
                        challenges.append(item.strip())
                        solutions.append("해결 방안: AI 기술과 데이터 분석을 활용한 자동화된 포트홀 관리 시스템 구축")
                else:
                    # 전체 텍스트를 하나의 도전 과제로 처리
                    challenges.append(challenge_text.strip())
                    solutions.append("해결 방안: AI 기술과 데이터 분석을 활용한 자동화된 포트홀 관리 시스템 구축")
                break
    except Exception as e:
        print(f"README 파싱 중 오류 발생: {str(e)}")
    
    return features, challenges, solutions

def extract_github_info(repo_url: str) -> dict:
    """Extract available information from GitHub repository."""
    try:
        match = re.match(r"https://github\.com/([^/]+)/([^/]+)", repo_url)
        if not match:
            return {}
        
        owner, repo_name = match.groups()
        repo = github.get_repo(f"{owner}/{repo_name}")
        
        # Extract basic repository information
        github_info = {
            "repositoryUrl": repo_url,
            "branchStructure": ", ".join([branch.name for branch in repo.get_branches()]),
            "contributionStats": f"Total commits: {repo.get_commits().totalCount}"
        }
        
        # Extract technical information from languages
        languages = repo.get_languages()
        tech_info = {
            "frontendTech": [],
            "backendTech": [],
            "database": [],
            "deployment": [],
            "otherTools": []
        }
        
        # Categorize technologies
        for lang in languages:
            if lang.lower() in ['javascript', 'typescript', 'html', 'css', 'react', 'vue', 'angular']:
                tech_info["frontendTech"].append(lang)
            elif lang.lower() in ['python', 'java', 'go', 'ruby', 'php', 'node']:
                tech_info["backendTech"].append(lang)
            elif lang.lower() in ['sql', 'mysql', 'postgresql', 'mongodb']:
                tech_info["database"].append(lang)
            else:
                tech_info["otherTools"].append(lang)
        
        return {
            "githubInfo": github_info,
            "technicalInfo": tech_info
        }
    except Exception as e:
        print(f"GitHub 정보 추출 중 오류 발생: {str(e)}")
        return {}

@mcp.tool()
def create_project_from_template(github_url: str = None) -> str:
    """Create a new project entry using the template structure."""
    try:
        # Load template
        template = load_template()
        
        # If GitHub URL is provided, extract available information
        if github_url:
            github_data = extract_github_info(github_url)
            template["projectInfo"]["githubInfo"] = github_data.get("githubInfo", {})
            template["projectInfo"]["technicalInfo"].update(github_data.get("technicalInfo", {}))
        
        # Set timestamps
        now = datetime.now().isoformat()
        template["timestamp"]["created"] = now
        template["timestamp"]["lastUpdated"] = now
        
        # Save to database
        conn = sqlite3.connect('portfolio.db')
        c = conn.cursor()
        c.execute('INSERT INTO projects (project_data) VALUES (?)',
                 (json.dumps(template),))
        project_id = c.lastrowid
        conn.commit()
        conn.close()
        
        return f"프로젝트 템플릿이 생성되었습니다. (ID: {project_id})\n필요한 정보를 입력해주세요."
    except Exception as e:
        return f"프로젝트 생성 중 오류 발생: {str(e)}"

@mcp.tool()
def get_project_info(project_id: int) -> str:
    """Get complete project information."""
    try:
        conn = sqlite3.connect('portfolio.db')
        c = conn.cursor()
        c.execute('SELECT project_data FROM projects WHERE id = ?', (project_id,))
        result = c.fetchone()
        conn.close()
        
        if not result:
            return f"프로젝트 ID {project_id}를 찾을 수 없습니다."
        
        return json.dumps(json.loads(result[0]), indent=2, ensure_ascii=False)
    except Exception as e:
        return f"프로젝트 정보 조회 중 오류 발생: {str(e)}"

if __name__ == "__main__":
    print("SSAFY Project Portfolio Server is running!") 