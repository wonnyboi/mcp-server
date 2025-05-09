# MCP 서버 API 문서

## 리소스

### 프로젝트 (Project)

```json
{
  "id": "string",
  "type": "string",
  "github_url": "string",
  "roles": ["string"],
  "basic_info": {},
  "technical_info": {},
  "achievements": {},
  "retrospective": {}
}
```

### 자기소개서 (Self Introduction)

```json
{
  "id": "string",
  "project_id": "string",
  "content": "string",
  "created_at": "string",
  "updated_at": "string"
}
```

### 면접 준비 (Interview Prep)

```json
{
  "id": "string",
  "project_id": "string",
  "questions": ["string"],
  "answers": ["string"],
  "feedback": ["string"]
}
```

## 도구 (Tools)

### GitHub 정보 추출

```python
def extract_github_info(github_url: str) -> dict:
    """
    GitHub 저장소에서 프로젝트 정보를 추출합니다.
    """
```

### 프로젝트 생성

```python
def create_project(project_type: str, github_url: str) -> dict:
    """
    새로운 프로젝트를 생성합니다.
    """
```

### 자기소개서 생성

```python
def create_self_introduction(project_id: str) -> dict:
    """
    프로젝트 정보를 기반으로 자기소개서를 생성합니다.
    """
```

### 면접 질문 생성

```python
def generate_interview_questions(project_id: str) -> list:
    """
    프로젝트 정보를 기반으로 면접 질문을 생성합니다.
    """
```

## 프롬프트 템플릿

### 프로젝트 정보 수집

```
프로젝트 유형: {project_type}
GitHub URL: {github_url}
역할: {roles}

다음 정보를 제공해주세요:
1. 프로젝트 기간
2. 주요 기술 스택
3. 핵심 기능
4. 본인의 기여도
```

### 면접 질문 생성

```
프로젝트: {project_name}
역할: {role}
기술 스택: {tech_stack}

다음 관점에서 면접 질문을 생성합니다:
1. 기술적 도전과제
2. 문제 해결 과정
3. 팀 협업 경험
4. 프로젝트 성과
```
