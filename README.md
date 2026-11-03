# AI & Maritime Brief — 무료 자동 게시·이메일 뉴스레터

## 원리
- 공개 Google 뉴스 RSS에서 지난 24시간 기사를 수집합니다.
- AI API를 이용하지 않습니다. **기사 본문을 읽고 AI로 요약한 결과가 아니라 RSS의 제목과 제공된 소개문**입니다. 소개문이 없으면 명시합니다.
- 매일 한국 시각 오전 8시 GitHub Actions가 HTML을 생성하고 GitHub Pages에 배포한 다음 Gmail로 동일한 HTML을 발송합니다.
- 사이트: https://gmlans77-ops.github.io/ai-maritime-news/
- **예약 실행은 GitHub 상황에 따라 지연/누락될 수 있습니다.** 뉴스 RSS의 품질이나 연결 상태에 따라 해당 날짜에 발행되지 않을 수 있습니다.

## 설치 — 지금 사용 중인 저장소에 추가
1. ZIP 압축을 풀고 안의 **내용물 전체**를 기존 `ai-maritime-news` 저장소에 업로드합니다. `archive/2026-11-03.html` 등 기존 파일은 유지하세요.
2. GitHub 브라우저에서 숨김 폴더 `.github/workflows`를 폴더째 올리기 어렵다면 **Add file → Create new file**을 선택하고 파일명에 `.github/workflows/daily-newsletter.yml`을 입력한 뒤 ZIP 파일의 해당 YAML 내용을 붙여넣으세요.
3. Settings → Actions → General → Workflow permissions → **Read and write permissions**를 선택할 수 있다면 설정하세요. 워크플로에도 `contents: write` 등이 포함되어 있습니다.
4. **매우 중요!** Settings → Pages → Build and deployment → Source를 기존 **Deploy from a branch**에서 **GitHub Actions**로 변경하세요. `GITHUB_TOKEN`이 만든 커밋은 branch-source Pages 빌드를 트리거하지 않으므로 이 변경이 필요합니다.
5. `Settings → Secrets and variables → Actions → New repository secret`에서 아래 세 가지를 각각 등록합니다. 앱 비밀번호를 **코드, README, 채팅에 절대 붙여넣지 마세요.**
   - `GMAIL_ADDRESS`: 발신할 **개인 Gmail 주소**
   - `GMAIL_APP_PASSWORD`: Google 계정의 **2단계 인증 → 앱 비밀번호**에서 생성한 16자리 비밀번호 (띄어쓰기 없이 입력)
   - `NEWSLETTER_TO`: 수신할 이메일 주소 (본인 개인 이메일 권장)
6. GitHub 저장소의 `Actions` → `Daily newsletter + website + email` → `Run workflow` → `Run workflow`를 눌러 한 번 시험 실행하세요. 수동 시험은 날짜 뒤에 `-test`가 붙은 별도의 뉴스레터를 만들므로 기존 1호를 덮어쓰지 않습니다.
7. 로그에서 `Generate HTML` → `Deploy GitHub Pages` → `Email HTML newsletter after deployment`가 성공인지 확인하고 개인 메일함(스팸함 포함)을 확인하세요.

## Gmail 앱 비밀번호
- https://myaccount.google.com/apppasswords 에서 생성할 수 있습니다(일부 계정에서는 사용 불가).
- 2단계 인증이 필요하며 개인용 Google 계정에만 사용하는 것을 권장합니다.
- 앱 비밀번호는 메일 전송 프로그램에 Gmail 계정 접근을 부여하므로 최소 권한 OAuth 방식보다 위험할 수 있습니다. 전용 개인 계정을 이용하고, 사용 중단 시 Google 계정에서 앱 비밀번호를 폐기하세요.

## GitHub Pages 참고
- GitHub Pages의 Source가 **GitHub Actions**인지 반드시 확인하세요. 이전 설정 `main/(root)` 상태를 그대로 두면 자동 게시 결과가 반영되지 않을 수 있습니다.
- 이 ZIP의 파일을 업로드하면 기존 1호 뉴스레터는 그대로 유지됩니다.
- 메일 발송은 **성공적으로 새 페이지가 배포된 후에만** 진행합니다. 새 기사가 없거나 같은 날 재실행하면 중복 메일을 보내지 않습니다.
- Google News RSS 원문 링크는 원 언론사 대신 Google 뉴스 중계 주소일 수 있습니다. 뉴스 발행일은 RSS 기준이며 진위·원문은 추가 확인하세요.

## 보안
- GitHub 저장소는 공개 상태입니다. 회사 기밀, 고객 정보, 사내 자료, 로그인 암호를 올리지 마세요.
- GitHub Secrets에만 암호를 저장하고, 커밋에 포함되지 않는지 확인하세요.
- 소스 피드의 내용은 신뢰할 수 없는 외부 텍스트이므로 HTML 이스케이프 후 표시합니다.

## 파일
- `generate_news.py`: RSS 수집, HTML 생성, 이메일 발송 코드
- `requirements.txt`: RSS 패키지
- `.github/workflows/daily-newsletter.yml`: 매일 자동 실행/배포/메일
- `index.html`: 기존 첫 페이지 디자인, 이후 자동 최신화
- `archive/`: 날짜별 보관
