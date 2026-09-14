# 나의 컨벤션 위키

C++ 코드와 Git 작업에서 반복되는 선택을 정리한 개인 개발 컨벤션입니다. 기존 스타일과 공식 자료를 비교해 규칙을 정리하며, C와 설계·빌드·품질 등의 주제로 확장합니다.

[위키 사이트](https://rniman.github.io/convention/) · [전체 목차](docs/index.md) · [컨벤션 적용 기준](docs/baseline.md)

## 문서 찾아보기

- [C++ 코딩 규칙](docs/coding/cpp/index.md): 명명, 포맷, 초기화, const, 주석, 헤더, 함수, 소유권·수명
- [Git·협업 규칙](docs/git/index.md): 커밋 메시지, 브랜치 명명

채택 범위와 변경 기록은 **컨벤션 적용 기준**에서 관리합니다. 나머지 분류와 각 문서의 후속·미결정 사항은 아직 채택된 규칙이 아닙니다.

## 저장소 구성

| 경로 | 역할 |
| --- | --- |
| [docs/](docs/index.md) | 주제별 컨벤션과 사이트의 Markdown 원본 |
| `ref/` | 과거 개인 자료. 로컬에 보존하며 Git 추적·사이트 빌드에서 제외 |
| [AGENTS.md](AGENTS.md) | 컨벤션 조사·편집 시 지킬 작업 지침 |
| [mkdocs.yml](mkdocs.yml) | 사이트 설정과 탐색 메뉴 |
| [scripts/](scripts/) | 빌드·미리보기와 사이트 변환 처리 |
| [.github/workflows/pages.yml](.github/workflows/pages.yml) | GitHub Pages 빌드·배포 |

문서를 추가하면 해당 분류의 `index.md`와 `mkdocs.yml`에 등록합니다. `docs/`의 Markdown을 직접 사용하고, 빌드 결과는 Git에서 제외된 `site/`에 생성합니다. 원문의 `ref/` 링크는 보존하며 사이트에서는 [site_hooks.py](scripts/site_hooks.py)가 로컬 참고 자료 표시로 바꿉니다.

## 로컬 미리보기와 검증

Windows PowerShell에서 저장소 루트를 기준으로 실행합니다.

최초 환경 준비:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
```

미리보기 실행:

```powershell
.venv/Scripts/python.exe scripts/build_site.py --serve
```

[로컬 미리보기](http://127.0.0.1:8000/convention/)에서 확인합니다. 문서를 저장하면 자동 갱신되며 `Ctrl+C`로 종료합니다.

배포 전 빌드 검증(`mkdocs build --strict`):

```powershell
.venv/Scripts/python.exe scripts/build_site.py
```

## 배포

`master`에 푸시하거나 [GitHub Actions](https://github.com/rniman/convention/actions)의 `Deploy convention wiki`를 수동 실행하면 빌드 검증 후 GitHub Pages에 배포합니다.

- 저장소 Settings → Pages → Build and deployment의 Source는 `GitHub Actions`를 사용합니다.
- 배포 실패 시 Actions에서 실패한 단계의 로그를 확인합니다.
- 배포 주소를 바꾸면 `mkdocs.yml`의 `site_url`과 이 문서의 사이트·미리보기 링크를 함께 확인합니다.

<details>
<summary>사이트 구성 참고 자료</summary>

아래는 기존 구성 시 확인한 자료입니다. 확인일: 2026-09-12.

- [MkDocs 설정·hooks](https://www.mkdocs.org/user-guide/configuration/#hooks)
- [Material for MkDocs 검색](https://squidfunk.github.io/mkdocs-material/setup/setting-up-site-search/)
- [Material for MkDocs 탐색](https://squidfunk.github.io/mkdocs-material/setup/setting-up-navigation/) · [추가 CSS](https://squidfunk.github.io/mkdocs-material/customization/#additional-css): 목차 표현은 [navigation.css](docs/stylesheets/navigation.css)에서 조정
- [GitHub Pages 사용자 지정 워크플로](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)

</details>
