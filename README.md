# MCP (My Career Portfolio) Server

SSAFY 학생들을 위한 프로젝트 포트폴리오 및 면접 준비 도우미 서버입니다.

## 주요 기능

1. 프로젝트 정보 수집

   - GitHub 저장소 연동
   - 프로젝트 정보 자동 수집
   - 역할별 상세 정보 수집

2. 자기소개서 작성 지원

   - 프로젝트 기반 자기소개서 작성
   - 자기소개서 수정 및 관리

3. 면접 준비

   - 프로젝트 기반 면접 질문 생성
   - 면접 답변 연습
   - 면접 피드백

4. 포트폴리오 작성
   - 프로젝트 기반 포트폴리오 작성
   - 포트폴리오 수정 및 관리

## 설치 방법

1. 저장소 클론

```bash
git clone https://github.com/your-username/mcp-server.git
cd mcp-server
```

2. 가상환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 의존성 설치

```bash
pip install -r requirements.txt
```

4. GitHub 토큰 설정

   - GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - 'Generate new token' 클릭
   - Note: 'MCP Portfolio Access' 입력
   - Expiration: 'No expiration' 선택
   - Select scopes: 'repo' 체크
   - 'Generate token' 클릭
   - 생성된 토큰을 복사
   - 프로젝트 루트 디렉토리에 '.env' 파일 생성
   - 다음 내용을 입력:
     ```
     GITHUB_TOKEN=your_github_token_here
     ```

5. 서버 실행

```bash
python project_portfolio_server.py
```

## 사용 방법

1. 프로젝트 추가

   - GitHub 저장소 URL 입력
   - 프로젝트 유형 선택
   - 역할 선택
   - 상세 정보 입력

2. 자기소개서 작성

   - 프로젝트 기반 자기소개서 작성
   - 수정 및 관리

3. 면접 준비

   - 프로젝트 기반 면접 질문 생성
   - 답변 연습
   - 피드백 수집

4. 포트폴리오 작성
   - 프로젝트 기반 포트폴리오 작성
   - 수정 및 관리

## 프로젝트 구조

```
mcp-server/
├── project_data/           # 프로젝트 데이터 저장
├── project_portfolio_server.py  # 메인 서버 파일
├── requirements.txt        # 의존성 목록
├── .env                   # 환경 변수 (GitHub 토큰)
└── README.md             # 프로젝트 설명
```

## 기여 방법

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 연락처

프로젝트 관리자 - [@your-username](https://github.com/your-username)

프로젝트 링크: [https://github.com/your-username/mcp-server](https://github.com/your-username/mcp-server)
