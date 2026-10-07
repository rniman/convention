# 나의 컨벤션 위키

C++ 코드와 Git 작업에서 반복되는 선택을 정리한 개인 개발 컨벤션입니다. 기존 스타일과 공식 자료를 비교해 규칙을 정리하며, C와 설계·빌드·품질 등의 주제로 확장합니다.

[위키 사이트](https://rniman.github.io/convention/) · [전체 목차](docs/index.md) · [컨벤션 적용 기준](docs/baseline.md)

## 문서 찾아보기

- [C++ 코딩 규칙](docs/coding/cpp/index.md): 포맷, 명명, 주석, 초기화, const, 헤더, 함수, 소유권·수명
- [Git·협업 규칙](docs/git/index.md): 커밋 메시지, 브랜치 명명
- [Unity 컨벤션 초안](docs/unity/index.md): 오브젝트·에셋 이름, 반복 번호와 기본 폴더 구조
- [RnimanEngine 프로젝트 정리](docs/projects/rniman-engine.md): 컨벤션 적용·핵심 제약과 주요 원본 문서 안내
- [위키의 적용과 프로젝트 근거 검토](docs/baseline.md#위키의-적용과-프로젝트-근거-검토): 프로젝트의 위키 확인·적용과 위키 정비 시 프로젝트 조사
- 공통화 초안: [검증 결과](docs/quality/verification.md) · [원본과 생성물](docs/git/artifacts.md)
- [HTML 기본 컨벤션 초안](docs/coding/html.md): 문서 골격·포맷·입력·접근성·JSX 차이. [Material Forge 참고 기록](docs/projects/material-forge.md)을 근거로 작성

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

사이트 글꼴은 [typography.css](docs/stylesheets/typography.css)에서 영역별로 지정합니다. 글꼴 원본을 `docs/assets/fonts/`에 포함해 사이트에서 직접 제공합니다.

| 영역 | 글꼴 | 출처·해시 | 라이선스 |
| --- | --- | --- | --- |
| 제목·메뉴·검색 등 인터페이스 | Pretendard Variable v1.3.9 | [원본 정보](docs/assets/fonts/pretendard/source.txt) | [OFL 1.1](docs/assets/fonts/pretendard/license.txt) |
| 본문·목록·표 | 리디바탕 1.0.1 | [원본 정보](docs/assets/fonts/ridibatang/source.txt) | [OFL 1.1](docs/assets/fonts/ridibatang/license.txt) |
| 코드 블록·인라인 코드·상단 메타정보 | D2Coding 1.4.0 일반판 | [원본 정보](docs/assets/fonts/d2coding/source.txt) | [OFL 1.1](docs/assets/fonts/d2coding/license.txt) |

Markdown의 YAML frontmatter는 MkDocs가 처리하는 메타데이터로 본문에 표시되지 않습니다. 코드 블록으로 보여주는 YAML과 문서 상단의 상태·적용 범위 안내에는 D2Coding을 적용합니다. 리디바탕은 Regular 한 굵기이며 본문의 굵은 강조는 브라우저가 합성합니다. D2Coding은 원본 Regular·Bold를 사용합니다.

라이선스 확인: Pretendard는 2026-10-06, 리디바탕·D2Coding은 2026-10-07. 공식 [Pretendard 라이선스](https://github.com/orioncactus/pretendard/blob/v1.3.9/LICENSE), [리디바탕 배포·라이선스 안내](https://ridicorp.com/ridibatang/), [D2Coding 1.4.0 배포](https://github.com/naver/d2-coding-font/releases/tag/VER1.4.0)와 [OFL FAQ 2.1](https://openfontlicense.org/ofl-faq/#2-using-ofl-fonts-for-webpages-and-online-webfont-services)을 확인했습니다. 웹폰트 사용·재배포 시 저작권 고지와 OFL 1.1 전문을 함께 제공하며, 글꼴 단독 판매와 수정본의 Reserved Font Name 제한을 따릅니다. 글꼴 데이터는 수정하지 않았고 원본 경로·SHA-256을 기록했습니다. 리디바탕 고지는 글꼴의 저작권 메타데이터와 공식 안내에 따른 OFL 전문을 수록했으며, 나머지는 공식 라이선스 파일을 보존합니다. 빌드 결과에도 글꼴·고지·라이선스를 포함합니다.

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
