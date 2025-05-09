# MCP 프로토콜 명세

## 개요

이 문서는 SSAFY 학생들을 위한 프로젝트 포트폴리오 및 면접 준비 도우미 서버의 MCP(Model Context Protocol) 구현을 설명합니다.

## 리소스 정의

### 1. 프로젝트 리소스

- GitHub 저장소 정보
- 프로젝트 기본 정보
- 기술 스택 정보
- 역할 및 성과 정보
- KPT 회고 정보

### 2. 자기소개서 리소스

- 프로젝트 기반 자기소개
- 역량 중심 자기소개
- 성과 중심 자기소개

### 3. 면접 준비 리소스

- 기술 면접 질문
- 프로젝트 면접 질문
- 답변 가이드

## 도구 (Tools)

### 1. GitHub 연동 도구

- 저장소 정보 추출
- 기술 스택 분석
- 컨트리뷰션 분석

### 2. 포트폴리오 도구

- 프로젝트 정보 수집
- 마크다운 문서 생성
- 진행 상태 추적

### 3. 면접 준비 도구

- 질문 생성
- 답변 검토
- 피드백 제공

## 프롬프트 템플릿

### 1. 프로젝트 정보 수집

- 역할별 맞춤형 질문
- 단계별 정보 수집
- 성과 중심 정보 추출

### 2. 자기소개서 작성

- 프로젝트 경험 기반
- STAR 기법 활용
- 역량 중심 작성

### 3. 면접 준비

- 기술 스택별 질문
- 프로젝트 심화 질문
- 답변 구조화 가이드

## 구현 가이드

### 1. 리소스 구현

```python
class Project(Resource):
    def __init__(self):
        self.github_info = {}
        self.basic_info = {}
        self.technical_info = {}
        self.achievements = {}
```

### 2. 도구 구현

```python
class GitHubTool(Tool):
    def extract_info(self, url: str):
        # GitHub API를 통한 정보 추출
        pass

    def analyze_tech_stack(self):
        # 기술 스택 분석
        pass
```

### 3. 프롬프트 구현

```python
class ProjectPrompt(Prompt):
    def generate_questions(self, role: str):
        # 역할별 질문 생성
        pass

    def process_response(self, response: str):
        # 응답 처리 및 저장
        pass
```

## 보안 고려사항

1. GitHub 토큰 관리
2. 사용자 데이터 보호
3. 접근 권한 제어

## 확장성

1. 데이터베이스 연동
2. 추가 외부 API 연동
3. 새로운 도구 추가
