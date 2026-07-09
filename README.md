# Schedule Editor (프로젝트 일정표 편집기)

해외출장 논의용 프로젝트 일정표(Gantt)를 회의 장소에서 바로 편집할 수 있는 도구입니다.
설치·인터넷 없이 브라우저에서 열리는 단일 HTML 파일이며, 각 단계별 Work Scope(작업 범위)와 납기일을 함께 관리합니다.

A self-contained, offline schedule (Gantt) editor for on-the-spot editing during meetings.
No install, no internet required — everything (including the PowerPoint export engine) is inlined in one HTML file.

## 구성 파일 / Files

| 파일 | 설명 |
|------|------|
| `Schedule_Editor_EN.html` | 편집기 — 영문판 (single-file, offline) |
| `Schedule_Editor.html` | 편집기 — 한글판 |
| `Schedule_Editor.xlsx` | 같은 일정표의 Excel 버전 (메일 첨부용, Start/End 입력 시 막대 자동 표시) |
| `run_editor.py` | 편집기를 데스크톱 앱(.exe)으로 실행/패키징하는 런처 |

## 사용법 / Usage

**HTML 편집기**
1. `Schedule_Editor_EN.html` (또는 한글판)을 더블클릭 → Chrome / Edge에서 열림
2. 막대를 끌어 이동 · 양끝을 끌어 기간 조절 · 빈 칸 클릭으로 막대 생성 · 더블클릭으로 삭제
3. 빨간 점선(납기일) 드래그로 이동
4. 각 단계의 Work Scope 입력
5. 저장: **JSON**(데이터), **HTML로 저장**(현재 일정이 담긴 자체 완결형 스냅샷), **PowerPoint 내보내기**, **인쇄/PDF**(막대 색상 포함)

**Excel 버전**
- `Start` / `End` 열에 분기 번호(1 = 2026 Q1 … 16 = 2029 Q4)를 입력하면 조건부 서식으로 막대가 자동 표시됩니다.
- `Work Scope` 시트에서 단계별 작업 범위를 입력 (기간 자동 계산).

## 데스크톱 앱(.exe)으로 빌드 / Build a desktop app

```bash
pip install pyinstaller
pyinstaller --onefile --name ScheduleEditor --add-data "Schedule_Editor_EN.html;." run_editor.py
```

`dist/ScheduleEditor.exe` 를 더블클릭하면 로컬 서버로 편집기를 띄우고 Edge 앱 창(주소창 없는 창)으로 엽니다.
실제 브라우저 엔진으로 실행되므로 다운로드·PowerPoint 내보내기가 정상 작동합니다.

## 주요 기능 / Features

- 드래그로 편집하는 Gantt 차트 — **분기(Quarter) / 월(Month) 단위 보기 전환** (연도 수 조절 가능)
- **Undo / Redo** (`Ctrl+Z` / `Ctrl+Y`), 단계 복제 (`Ctrl+D`), 순서 이동 (`Alt+↑/↓`)
- 막대를 클릭해 선택 후 **`Delete` 키로 삭제**
- **회사(기관)별 색상 지정** — 회사 목록(이름+색)을 만들고 각 단계에 지정하면 해당 막대가 그 색으로 표시
- 단계 추가/삭제·이름 편집, 납기/마일스톤 마커
- 단계별 Work Scope 상세 입력
- PowerPoint(.pptx) 내보내기 (Gantt + Work Scope, 회사 색상·이름 포함)
- 인쇄/PDF 시 막대 색상 그대로 출력 (landscape)
- 자체 완결형 HTML 스냅샷 저장 / JSON 저장·불러오기
- 완전 오프라인 (외부 의존성 없음)

### 키보드 단축키 / Keyboard shortcuts

| 단축키 | 동작 |
|--------|------|
| `Ctrl+Z` / `Ctrl+Y` | 실행취소 / 다시실행 (Undo / Redo) |
| `Delete` | 선택한 단계 삭제 |
| `Ctrl+D` | 선택한 단계 복제 |
| `Alt+↑` / `Alt+↓` | 단계 순서 위/아래로 이동 |
| `Esc` | 선택 해제 |
