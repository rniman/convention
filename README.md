# 나의 컨벤션 위키

개인 개발 컨벤션을 항목별로 정리하는 위키입니다.

현재 채택된 컨벤션은 C++ 코딩·설계 8개와 Git 2개, 총 10개 문서입니다.

- [컨벤션 적용 범위](docs/baseline.md)
- [전체 목차](docs/index.md)
- [C++ 코딩 규칙](docs/coding/cpp/index.md)
- [설계 규칙](docs/design/index.md)
- [Git·협업 규칙](docs/git/index.md)

기존 자료는 `ref/`에 보존하며 새 규칙의 근거로만 참고합니다.

## 사이트 관리

- [문서 사이트](https://rniman.github.io/convention/)
- 원본은 이 저장소의 Markdown이며, `main`에 푸시하면 자동 배포됩니다.
- 로컬 빌드: `python -m pip install -r requirements.txt` 후 `python scripts/build_site.py`
- 빌드 결과는 `site/`, 임시 원본 묶음은 `.site-src/`에 생성하며 Git에서 제외합니다.
- 새 페이지를 추가하면 분류 목차와 `mkdocs.yml`의 탐색 메뉴를 함께 갱신합니다.
- 배포 설정: GitHub 저장소의 Settings → Pages → Source에서 GitHub Actions를 선택합니다.

사이트 구성 참고: [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/),
[GitHub Pages 배포](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
확인일: 2026-09-12. 사용 버전은 `requirements.txt`에 고정합니다.
