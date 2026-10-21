# Genie's Water Studybook — K-water 기사 자동 업데이트

이 폴더는 **뉴스 전용**이에요. 공개 저장소에는 기사 제목·링크만 올립니다.
**절대 넣으면 안 되는 것**: 개인 대시보드 HTML, 자소서, 경험자료, 메모, S펜 필기, Firebase 비공개 키, 학습 백업 JSON.

## 따라 하기

### 1) GitHub 저장소 만들기
- https://github.com/new 접속해 GitHub로 로그인 (없다면 회원가입).
- Repository name에 `kwater-issue-feed` 입력.
- **Public** 선택, `Create repository` 클릭.
- GitHub Free 공개 저장소에서 GitHub Pages·기본 Actions를 무료로 이용할 수 있습니다(서비스 정책/한도 변경 가능).

### 2) 파일 업로드
- 새 저장소에서 `Add file` → `Upload files`.
- 이 압축파일을 먼저 **압축 풀기**. 안에 있는 `collect_news.py`, `news-data.json`, `.github` 폴더를 모두 드래그해 업로드.
- `.github/workflows/refresh_news.yml`이 저장소에 반드시 있는지 확인하세요.
- 아래쪽 `Commit changes` 클릭. (README.md도 함께 올려도 됩니다.)
- GitHub 웹 화면에서 `.github` 폴더 드래그가 안 되면 `Add file → Create new file`에서 파일 이름을 `.github/workflows/refresh_news.yml`로 입력하고 압축 속 같은 파일 내용을 복사해 저장하면 됩니다.

### 3) GitHub Pages 사용 설정
- 저장소 상단 `Settings` → 왼쪽 `Pages`.
- `Build and deployment` → `Source`를 **GitHub Actions**로 선택.
  (중요: 예전 안내의 `Deploy from a branch`가 아니라 `GitHub Actions`로 설정해야 예약 뉴스가 게시됩니다.)

### 4) 첫 뉴스 수집 시작
- 저장소 상단 `Actions` → 왼쪽 `Refresh K-water issue headlines` 선택.
- `Run workflow` → `Run workflow` 클릭.
- 실행 기록 옆 녹색 체크가 뜨면 첫 뉴스 수집·게시가 완료된 것입니다.
- `https://<본인GitHub아이디>.github.io/kwater-issue-feed/news-data.json` 을 새 탭에서 확인.
- `404`이면 몇 분 기다려 새로고침해 보세요. GitHub Pages 설정 및 Actions 성공 여부를 다시 확인하세요.

### 5) 기존 Firebase 학습 대시보드에 연결
- https://genies-water-studybook.web.app/ 접속 후 로그인.
- `최신 이슈 브리핑` → `⚙ 뉴스 연결`.
- 위의 `https://.../news-data.json` 주소를 입력하고 `주소 저장 및 불러오기` 클릭.
- 새로 불러온 기사 제목·출처·게시일을 확인하세요. 자동 분류는 **학습용**이며 사실 검증이 아니므로 원문을 열어 확인해야 합니다.

## 자동 갱신과 주의사항
- 실행 예약: 한국시간 **매일 오전 9:27 / 오후 9:27**, GitHub 실행 지연 가능. 대시보드는 사이트를 열거나 `↻ 새 소식 확인` 버튼을 누를 때 최신 JSON을 읽습니다.
- Google 뉴스 RSS 검색 결과에서 제목·날짜·출처·기사 링크만 수집합니다. **K-water 공식 보도자료 전체를 직접 수집하는 버전이 아니며**, 공식 보도자료는 별도 검증이 필요합니다.
- 공개 GitHub 저장소와 GitHub Pages에서는 뉴스 메타데이터를 다른 사람이 볼 수 있습니다. 개인 학습 데이터는 Firebase에 따로 저장합니다.
- GitHub 공개 저장소라도 60일간 활동이 없으면 예약된 워크플로가 비활성화될 수 있습니다.
- 원문 사이트의 접근 제한, RSS 정책 변경, GitHub 실행 실패 등에 따라 갱신이 멈출 수 있습니다.
- PC와 태블릿의 `뉴스 연결 주소`는 브라우저별로 각각 입력해야 할 수 있습니다.

## 오류 체크
- Actions 탭에 워크플로가 없으면 `.github/workflows/refresh_news.yml` 파일 경로를 확인.
- `git push` 거부면 `Settings → Actions → General → Workflow permissions`의 쓰기 권한 허용 여부 확인.
- Pages 배포 실패면 `Settings → Pages`에서 Source가 **GitHub Actions**인지 확인.
- JSON은 보이는데 대시보드에 기사가 없으면 `뉴스 연결`에 붙인 주소가 `https://`로 시작하고 `news-data.json`으로 끝나는지 확인.
