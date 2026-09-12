# 나의 컨벤션 위키

개인 개발 컨벤션을 항목별로 정리하는 위키입니다.

현재 채택된 컨벤션은 C++ 코딩 8개와 Git 2개, 총 10개 문서입니다.

- [컨벤션 적용 범위](docs/baseline.md)
- [전체 목차](docs/index.md)
- [C++ 코딩 규칙](docs/coding/cpp/index.md)
- [설계 목차·정리 범위](docs/design/index.md)
- [Git·협업 규칙](docs/git/index.md)

기존 자료는 `ref/`에 보존하며 새 규칙의 근거로만 참고합니다.

## 사이트 관리

[위키 사이트](https://rniman.github.io/convention/) · [GitHub 저장소](https://github.com/rniman/convention)

`master`에 푸시하거나 Actions의 `Deploy convention wiki`를 수동 실행하면 빌드 검증 후 GitHub Pages에 배포합니다. 워크플로는 `.github/workflows/pages.yml`에서 관리합니다.

Windows PowerShell에서 저장소 루트를 기준으로 실행합니다.

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe scripts/build_site.py --serve
```

[로컬 미리보기](http://127.0.0.1:8000/convention/)에서 확인하며, 실행한 터미널에서 `Ctrl+C`로 종료합니다. 문서를 저장하면 미리보기가 자동 갱신됩니다.

배포용 빌드 검증:

```powershell
.venv/Scripts/python.exe scripts/build_site.py
```

- `docs/`의 Markdown을 직접 원본으로 사용하고 결과는 Git에서 제외된 `site/`에 생성합니다.
- 새 페이지를 추가하면 분류 목차와 `mkdocs.yml`의 탐색 메뉴를 함께 갱신합니다.
- `ref/`는 Git 추적과 사이트 빌드 모두에서 제외합니다. 원본 Markdown의 참고 링크는 보존하며, 사이트에서는 `scripts/site_hooks.py`가 로컬 참고 자료 표시로 바꿉니다.
- GitHub Settings → Pages → Build and deployment의 Source는 `GitHub Actions`를 사용합니다.
- 배포 실패 시 저장소 Actions에서 실패한 빌드·배포 로그를 확인합니다.
- 배포 주소를 바꾸면 `mkdocs.yml`의 `site_url`과 이 안내를 함께 갱신합니다.

구성 근거: [MkDocs 설정·hooks](https://www.mkdocs.org/user-guide/configuration/#hooks), [Material for MkDocs 검색 설정](https://squidfunk.github.io/mkdocs-material/setup/setting-up-site-search/). 확인일: 2026-09-12.

배포 구성 근거: [GitHub Pages 사용자 지정 워크플로](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages). 확인일: 2026-09-12.
