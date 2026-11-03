# AI & Maritime Brief — GitHub Pages 실습

ChatGPT Plus의 예약 작업으로 매일 뉴스 요약을 받고, GitHub Pages에는 사용자가 직접 HTML을 올리는 **API 비용 0원** 방식입니다. (GitHub 무료 공개 저장소 사용)

## 첫 게시 (처음 한 번)
1. https://github.com 에서 개인 계정으로 로그인합니다.
2. 오른쪽 `+` → **New repository** → 이름 `ai-maritime-news` → **Public** → **Create repository**.
3. 저장소 화면에서 **uploading an existing file** 또는 **Add file → Upload files**를 선택합니다.
4. 이 ZIP의 `index.html`, `.nojekyll`, `archive/2026-11-03.html`을 **폴더 구조 그대로** 올립니다. GitHub 업로드 화면에서는 폴더 `archive`를 통째로 드래그하면 편합니다. `README.md`도 같이 올려도 됩니다. 폴더 업로드가 안 되면 새 파일 만들기에서 파일명을 `archive/2026-11-03.html`로 지정하고 내용을 붙여넣습니다.
5. 아래 **Commit changes**를 누릅니다.
6. **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: main, /(root) → Save**.
7. 몇 분 후 `https://내아이디.github.io/ai-maritime-news/`에서 확인합니다. GitHub Pages 게시 시간이 지연될 수 있습니다.

## 매일 업데이트 (수동, API 비용 없음)
1. 매일 오전 8시 ChatGPT 예약 작업의 뉴스를 확인합니다. 요약은 자동 수신되지만 HTML 파일이 자동 생성·게시되는 것은 보장되지 않습니다.
2. ChatGPT에 다음처럼 요청합니다:
   > 오늘 받은 AI·조선해운 뉴스레터를 검토해 공개 기사와 원문 URL을 확인한 뒤, GitHub Pages용 `archive/YYYY-MM-DD.html` 파일을 만들어 줘. 그리고 최신 발행물 링크가 맨 위에 오도록 `index.html`도 업데이트해 줘. 두 파일을 내려받을 수 있게 해 줘.
3. 받은 `YYYY-MM-DD.html`을 저장소의 `archive/` 폴더에 업로드하고, **기존 `index.html`을 새 버전으로 교체**합니다. (기존 `index.html` 파일 화면의 연필 아이콘으로 편집하거나 업로드로 대체)
4. **Commit changes**를 누르고 페이지에서 새로운 날짜가 보이는지 확인합니다.
5. 새로운 기사 내용을 확인한 뒤에 공개하세요. ChatGPT의 뉴스 요약에는 오류가 있을 수 있습니다.

## 파일 구조
```
ai-maritime-news/
├── index.html                 # 웹사이트 첫 화면 / 뉴스레터 목록
├── .nojekyll                  # 정적 파일 그대로 게시
├── README.md                  # 이 안내서
└── archive/
    └── 2026-11-03.html        # 첫 번째 뉴스레터
```

## 보안
GitHub Pages는 인터넷에 공개됩니다. 회사 도면, 고객 정보, 이메일, 회의록, 개인 식별 정보 등 비공개 자료는 절대로 업로드하지 마세요. 회사 PC 사용 가능 여부는 사내 정책을 먼저 확인하세요.

## 비용 / 한계
GitHub Pages는 GitHub Free의 공개 저장소로 무료 사용 가능하며, 이번 구성은 OpenAI API를 사용하지 않습니다. ChatGPT Plus 구독과 사용량 한도는 적용됩니다. **자동 수집·알림은 ChatGPT**, **HTML 생성 요청과 게시 작업은 사용자**가 담당합니다.
